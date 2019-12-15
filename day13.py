import argparse
import os
from itertools import permutations
parser = argparse.ArgumentParser(description="AoC day 13")
parser.add_argument("file", help="The file that should be sourced")
parser.add_argument("-p", "--phase", help="The part of the exercise that we are at", type=int, default=1)
parser.add_argument("-t", "--target", help="A target value being aimed for", type=int, default=0)


def main(argv):
    print(f"test, {argv}")

    infile = open(argv.file, "r")

    allItems = []

    for line in infile:
        # do a line operation
        if line:
            allItems.append(line)

    infile.close()

    # commands require a little more processing
    commands = []
    for item in allItems:
        numSet = str.split(item, ',')
        for x in numSet:
            commands.append(int(x))

    if argv.phase == 1:
        sol = solutionPt1(commands)
        print(f"Total was {sol}")
    elif argv.phase == 2:
        sol = solutionPt2(commands)
        print(f"Final score: {sol}")

def insert_into_screen(x, y, id, screen_buffer):
    if id is None:
        return
    if y not in screen_buffer:
        screen_buffer[y] = {x: id}
        return
    else:
        screen_buffer[y][x] = id
        return

def display_screen_buffer(screen_buffer, last_state):
    ymax = max(screen_buffer.keys())
    xmax = 100
    os.system("cls")

    # nothing, box, block, paddle, ball
    sprites = [' ', u"\u25A1", 'H', '=', 'o']

    ball = last_state[0]
    paddle = last_state[1]
    for j in range(0, ymax + 1):
        for i in range(0, xmax + 1):
            if j in screen_buffer.keys() and i in screen_buffer[j].keys():
                pixel = screen_buffer[j][i]
                char = sprites[pixel]
                print(char, end='', flush=True)
                if pixel == 4:
                    ball = i, j
                if pixel == 3:
                    paddle = i, j
        print()
    if 0 in screen_buffer.keys() and -1 in screen_buffer[0].keys():
        print(f"score: {screen_buffer[0][-1]}")


    joystick = 0
    vert = ball[1] - last_state[0][1]
    if vert> 1 or vert < -1:
        return ball, paddle, joystick

    if vert < 0:
        # follow ball generically going upward
        trend = ball[0] - paddle[0]
        if trend > 0:
            joystick = 1
        elif trend < 0:
            joystick = -1
        elif trend == 0:
            old_trend = ball[0] - last_state[0][0]
            if old_trend > 0:
                joystick = 1
            elif old_trend < 0:
                joystick = -1
        else:
            joystick = 0
    elif vert > 0:
        # going down, we want to be at a target
        slope = ball[0] - last_state[0][0], ball[1] - last_state[0][1]
        ghost = ball[0], ball[1]
        while ghost[1] != paddle[1] - 1:
            ghost = ghost[0] + slope[0], ghost[1] + slope[1]
        if paddle[0] < ghost[0]:
            joystick = 1
        elif paddle[0] > ghost[0]:
            joystick = -1
        else:
            joystick = 0
    else:
        joystick = 0

    return ball, paddle, joystick


def solutionPt1(commands):

    # y -> x -> id
    screen_buffer = {}

    comp = Computer(commands, halting_output=True)

    # comp.insert_pipeline(painted)
    first_run = True
    while comp.is_running() or first_run:
        first_run = False
        comp.run(restart=False)
        comp.run(restart=False)
        comp.run(restart=False)
        insert_into_screen(comp.read_pipeline(), comp.read_pipeline(), comp.read_pipeline(), screen_buffer)

    print("game done")
    blocks = 0
    for j in screen_buffer.keys():
        for i in screen_buffer[j].keys():
            if screen_buffer[j][i] == 2:
                blocks += 1

    return blocks


def solutionPt2(commands):

    # y -> x -> id
    screen_buffer = {}

    comp = Computer(commands, halting_output=True)

    # comp.insert_pipeline(painted)
    first_run = True
    cur_state = (0, 0), (0, 0), 0
    out_stack = []
    while comp.is_running() or first_run:
        first_run = False

        # inject_input(comp, cur_state)
        comp.run(restart=False)
        inject_input(comp, cur_state)
        if comp.cur_state.paused_for_stream:
            out_stack.append(comp.read_pipeline())
        if len(out_stack) == 3:
            insert_into_screen(out_stack[0], out_stack[1], out_stack[2], screen_buffer)
            cur_state = display_screen_buffer(screen_buffer, cur_state)
            out_stack = []

    print("game done")

    return screen_buffer[0][-1]


def inject_input(comp, cur_state):
    if comp.cur_state.paused_for_input:
        comp.insert_pipeline(cur_state[2])


##############################################################
##################### NO TOUCH ###############################

class Computer:
    # a 'none' input is a user input halt
    def __init__(self, program, prog_input=None, halting_output=False):
        self.program_orig = program
        self.output = []
        self.halting_output = halting_output

        self.inpipe = []
        self.outpipe = []
        self.cur_state = None

    def reset(self):
        self.output = []
        self.input = [None]
        self.cur_state = None
        # for i in range(0, len(self.program_orig)):
        #     self.program[i] = self.program_orig[i]

    def run(self, restart=True):
        if self.cur_state is None or restart:
            self.cur_state = progState()
            self.cur_state.turing = self.program_orig

        if self.cur_state.paused_for_stream:
            self.cur_state.paused_for_stream = False

        while self.cur_state.running:
            self.cur_state = self._parseCodes(self.cur_state)
            if self.cur_state.errored:
                print(f"irregular execution at pointer {self.cur_state.progPointer}")
            if self.cur_state.paused_for_input or self.cur_state.paused_for_stream:
                return self.cur_state.turing

        return self.cur_state.turing

    def is_running(self):
        if self.cur_state is None:
            return False
        return self.cur_state.running

    def insert_pipeline(self, thing):
        self.inpipe = [int(thing)]

    def read_pipeline(self):
        if len(self.outpipe) > 0:
            # print(f" popped {self.outpipe[-1]}")
            return self.outpipe.pop()
        else:
            return None

    def _getModes(self, number):
        return int(int(number % 1000 / 100)), int(number % 10000 / 1000), int(number / 10000)

    def _getOp(self, number):
        return int(number % 100)

    def _grow_mem(self, state, spot):
        if spot >= len(state.turing):
            growth = spot - len(state.turing)
            for i in range(0, growth+2):
                state.turing.append(0)
        return state


    def _parseCodes(self, curState):
        opd = curState.clone()
        command = self._getOp(curState.turing[curState.progPointer])
        # mode 0 positional, 1 immediate
        mode = self._getModes(curState.turing[curState.progPointer])

        # print(f"pointer at {curState.progPointer}")
        # print(f"command is {command}")
        # print(f"mode is {mode}")
        # print(f"program is {curState.turing}")

        # 0 address mode
        # 1 immediate mode
        # 2 relative (offset) mode
        loc = 0
        if command in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if mode[0] == 0:
                loc = opd.turing[opd.progPointer + 1]
            elif mode[0] == 1:
                loc = opd.progPointer + 1
            elif mode[0] == 2:
                loc = opd.relative_base + opd.turing[opd.progPointer + 1]
            opd = self._grow_mem(opd, loc)
            paramA = opd.turing[loc]
        paramA_loc = loc

        loc = 0
        if command in [1, 2, 5, 6, 7, 8]:
            if mode[1] == 0:
                loc = opd.turing[opd.progPointer + 2]
            elif mode[1] == 1:
                loc = opd.progPointer + 2
            elif mode[1] == 2:
                loc = opd.relative_base + opd.turing[opd.progPointer + 2]
            opd = self._grow_mem(opd, loc)
            paramB = opd.turing[loc]
        paramB_loc = loc

        loc = 0
        if command in [1, 2, 7, 8]:
            if mode[2] == 0:
                loc = opd.turing[opd.progPointer + 3]
            elif mode[2] == 1:
                opd.errored = True
                opd.running = False
                print("Illegal write mode *immediate*")
                return opd
            elif mode[2] == 2:
                loc = opd.relative_base + opd.turing[opd.progPointer + 3]
            opd = self._grow_mem(opd, loc)
        paramC_loc = loc

        if command == 1:
            # Add from first two positions, store in the third
            opd.turing[paramC_loc] = paramA + paramB
            opd.progPointer += 4
        elif command == 2:
            # Add from first two positions, store in the third
            opd.turing[paramC_loc] = paramA * paramB
            opd.progPointer += 4
        elif command == 3:
            # take input
            if opd.paused_for_input:
                opd.turing[paramA_loc] = self.inpipe.pop()
                opd.paused_for_input = False
            else:
                if len(self.inpipe) == 1:
                    opd.turing[paramA_loc] = self.inpipe.pop()
                    opd.paused_for_input = False
                else:
                    opd.paused_for_input = True
                    return opd
            opd.progPointer += 2
        elif command == 4:
            # output to buffer
            self.outpipe.insert(0, paramA)
            opd.progPointer += 2
            if self.halting_output:
                opd.paused_for_stream = True
                return opd
        elif command == 5:
            # first value not zero, set pointer to second val
            opd.progPointer = paramB if paramA != 0 else opd.progPointer + 3
        elif command == 6:
            # first value zero, set pointer to second val
            opd.progPointer = paramB if paramA == 0 else opd.progPointer + 3
        elif command == 7:
            # if first param is less than second, store 1 in third, otherwise 0
            opd.turing[paramC_loc] = 1 if paramA < paramB else 0
            opd.progPointer += 4
        elif command == 8:
            # if first param is equal to second, store 1 in third, otherwise 0
            opd.turing[paramC_loc] = 1 if paramA == paramB else 0
            opd.progPointer += 4
        elif command == 9:
            # add to the prog's relative base
            opd.relative_base += paramA
            opd.progPointer += 2
        elif command == 99:
            # halt
            opd.running = False
            # print("--FINISH--")
        else:
            # error
            opd.running = False
            opd.errored = True

        return opd


class progState:
    def __init__(self):
        self.progPointer = 0
        self.turing = []
        self.running = True
        self.errored = False
        self.paused_for_input = False
        self.paused_for_stream = False
        self.relative_base = 0

    def clone(self):
        temp = progState()
        temp.progPointer = self.progPointer
        temp.running = self.running
        temp.turing = self.turing.copy()
        temp.paused_for_input = self.paused_for_input
        temp.paused_for_stream = self.paused_for_stream
        temp.relative_base = self.relative_base
        return temp


def digit_splitter(num, min_size=1):
    sign = 1
    digits = []
    if num < 0:
        sign = -1
        num = abs(num)
    place = 1
    while num > place:
        digits.append(int(num % (place * 10) / place) * sign)
        place *= 10

    while len(digits) < min_size:
        digits.append(0)
    digits.reverse()
    return digits

##################### NO TOUCH ###############################
##############################################################

main(parser.parse_args())