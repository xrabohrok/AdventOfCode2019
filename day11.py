import argparse
from itertools import permutations
parser = argparse.ArgumentParser(description="AoC day 11")
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
        print(f"Total was {sol[0]}")
    elif argv.phase == 2:
        solutionPt2(commands)


##############################################################
##################### NO TOUCH ###############################

class Computer:
    # a 'none' input is a user input halt
    def __init__(self, program, prog_input=None):
        self.program_orig = program
        self.input_counter = 0
        self.output = []

        self.inpipe = []
        self.outpipe = []
        self.cur_state = None

    def reset(self):
        self.input_counter = 0
        self.output = []
        self.input = [None]
        self.cur_state = None
        # for i in range(0, len(self.program_orig)):
        #     self.program[i] = self.program_orig[i]

    def run(self, restart=True):
        if self.cur_state is None or restart:
            self.cur_state = progState()
            self.cur_state.turing = self.program_orig

        while self.cur_state.running:
            self.cur_state = self._parseCodes(self.cur_state)
            if self.cur_state.errored:
                print(f"irregular execution at pointer {self.cur_state.progPointer}")
            if self.cur_state.paused_for_input:
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
        self.relative_base = 0

    def clone(self):
        temp = progState()
        temp.progPointer = self.progPointer
        temp.running = self.running
        temp.turing = self.turing.copy()
        temp.paused_for_input = self.paused_for_input
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


def turn(direction, turn_dir):
    if turn_dir == 0:
        direction -= 1
    else:
        direction += 1
    direction = direction % 4

    vec = 0,0
    if direction == 0:
        vec = 0, 1
    elif direction == 1:
        vec = 1, 0
    elif direction == 2:
        vec = 0, -1
    elif direction == 3:
        vec = -1, 0

    return direction, vec


def solutionPt1(items):

    # up is 0, count clockwise to 3
    direction = 0

    pos = 0, 0
    vec = 0, 0

    grid = {}

    comp = Computer(items.copy())

    firstrun = True
    while comp.is_running() or firstrun:
        if pos[0] not in grid.keys():
            grid[pos[0]] = {}
        if pos[1] not in grid[pos[0]].keys():
            grid[pos[0]][pos[1]] = 0
            painted = 0
        else:
            painted = grid[pos[0]][pos[1]]

        comp.insert_pipeline(painted)
        comp.run(restart=False)
        firstrun = False

        new_com = comp.read_pipeline(), comp.read_pipeline()

        # paint
        grid[pos[0]][pos[1]] = new_com[0]

        # turn
        turn_response = turn(direction, new_com[1])
        direction = turn_response[0]
        vec = turn_response[1]

        # move
        pos = pos[0] + vec[0], pos[1] + vec[1]

    total = 0
    for i in grid.keys():
        for j in grid[i].keys():
            if grid[i][j] >= 0:
                total += 1

    return total, grid


def solutionPt2(items):

    # up is 0, count clockwise to 3
    direction = 0

    pos = 0, 0
    vec = 0, 0

    grid = {}
    # start on white tile
    grid[0] = {}
    grid[0][0] = 1

    comp = Computer(items.copy())

    firstrun = True
    while comp.is_running() or firstrun:
        if pos[0] not in grid.keys():
            grid[pos[0]] = {}
        if pos[1] not in grid[pos[0]].keys():
            grid[pos[0]][pos[1]] = 0
            painted = 0
        else:
            painted = grid[pos[0]][pos[1]]

        comp.insert_pipeline(painted)
        comp.run(restart=False)
        firstrun = False

        new_com = comp.read_pipeline(), comp.read_pipeline()

        # paint
        grid[pos[0]][pos[1]] = new_com[0]

        # turn
        turn_response = turn(direction, new_com[1])
        direction = turn_response[0]
        vec = turn_response[1]

        # move
        pos = pos[0] + vec[0], pos[1] + vec[1]

    total = 0
    for i in grid.keys():
        for j in grid[i].keys():
            if grid[i][j] >= 0:
                total += 1

    x_min = min(grid.keys())
    x_max = max(grid.keys())
    y_min = 0
    y_max = 0

    for x in grid.keys():
        y_max_temp = max(grid[x].keys())
        y_min_temp = min(grid[x].keys())
        if y_max_temp > y_max:
            y_max = y_max_temp
        if y_min_temp < y_min:
            y_min = y_min_temp

    for y in range(y_min, y_max+1):
        print('')
        for x in range(x_min, x_max +1):
            if x in grid.keys() and y in grid[x].keys():
                if grid[x][y] >= 1:
                    print(f"{grid[x][y]}", end='', flush=True)
                else:
                    print(f" ", end='', flush=True)
            else:
                print(f" ", end='', flush=True)

    return total, grid


main(parser.parse_args())

