import argparse
from itertools import permutations
parser = argparse.ArgumentParser(description="AoC day 5")
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
        print(f"\nBiggest output is {sol[0]} at {sol[1]}")


# Opcode 1 adds together numbers read from two positions and stores the result in a third position.
# The three integers immediately after the opcode tell you these three positions
# - the first two indicate the positions from which you should read the input values,
# and the third indicates the position at which the output should be stored.

# Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them.
# Again, the three integers after the opcode indicate where the inputs and outputs are, not their values.

# Opcode 3 takes a single integer as input and saves it to the address given by its only parameter.
# For example, the instruction 3,50 would take an input value and store it at address 50.

# Opcode 4 outputs the value of its only parameter.
# For example, the instruction 4,50 would output the value at address 50.

# Opcode 5 is jump-if-true: if the first parameter is non-zero,
# it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.

# Opcode 6 is jump-if-false: if the first parameter is zero,
# it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.

# Opcode 7 is less than: if the first parameter is less than the second parameter,
# it stores 1 in the position given by the third parameter. Otherwise, it stores 0.

# Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.

# 99 means that the program is finished and should immediately halt.

class Computer:
    # a 'none' input is a user input halt
    def __init__(self, program, prog_input=None):
        self.program_orig = program
        self.program = self.program_orig.copy()
        if prog_input is None:
            self.input = [None]
        self.input_counter = 0
        self.output = []

    def reset(self):
        self.input_counter = 0
        self.output = []
        self.program = self.program_orig.copy()
        self.input = [None]
        # for i in range(0, len(self.program_orig)):
        #     self.program[i] = self.program_orig[i]

    def run(self):
        program = progState()
        program.turing = self.program
        while program.running:
            program = self._parseCodes(program)
            if program.errored:
                print(f"irregular execution at pointer {program.progPointer}")

        return program.turing

    def _getModes(self, number):
        return int(int(number % 1000 / 100)), int(number % 10000 / 1000), int(number / 10000)

    def _getOp(self, number):
        return int(number % 100)

    def _parseCodes(self, curState):
        opd = curState.clone()
        command = self._getOp(curState.turing[curState.progPointer])
        # mode 0 positional, 1 immediate
        mode = self._getModes(curState.turing[curState.progPointer])

        # print(f"pointer at {curState.progPointer}")
        # print(f"command is {command}")
        # print(f"mode is {mode}")
        # print(f"program is {curState.turing}")

        paramA = 0
        if command in [1, 2, 3, 4, 5, 6, 7, 8]:
            paramA = opd.turing[opd.turing[opd.progPointer + 1]] if mode[0] == 0 else opd.turing[opd.progPointer + 1]
        paramB = 0
        if command in [1, 2, 5, 6, 7, 8]:
            paramB = opd.turing[opd.turing[opd.progPointer + 2]] if mode[1] == 0 else opd.turing[opd.progPointer + 2]

        if command == 1:
            # Add from first two positions, store in the third
            opd.turing[opd.turing[opd.progPointer + 3]] = paramA + paramB
            opd.progPointer += 4
        elif command == 2:
            # Add from first two positions, store in the third
            opd.turing[opd.turing[opd.progPointer + 3]] = paramA * paramB
            opd.progPointer += 4
        elif command == 3:
            # take input
            if self.input[self.input_counter] is None:
                print("HALT---AWAITING INPUT:")
                opd.turing[opd.turing[opd.progPointer + 1]] = int(input())
            else:
                opd.turing[opd.turing[opd.progPointer + 1]] = self.input[self.input_counter]
            if self.input_counter < len(self.input) - 1:
                self.input_counter += 1
            opd.progPointer += 2

        elif command == 4:
            # output to buffer
            self.output.append(paramA)
            opd.progPointer += 2
        elif command == 5:
            # first value not zero, set pointer to second val
            opd.progPointer = paramB if paramA != 0 else opd.progPointer + 3
        elif command == 6:
            # first value zero, set pointer to second val
            opd.progPointer = paramB if paramA == 0 else opd.progPointer + 3
        elif command == 7:
            # if first param is less than second, store 1 in third, otherwise 0
            opd.turing[opd.turing[opd.progPointer + 3]] = 1 if paramA < paramB else 0
            opd.progPointer += 4
        elif command == 8:
            # if first param is equal to second, store 1 in third, otherwise 0
            opd.turing[opd.turing[opd.progPointer + 3]] = 1 if paramA == paramB else 0
            opd.progPointer += 4
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
    progPointer = 0
    turing = []
    running = True
    errored = False

    def clone(self):
        temp = progState()
        temp.progPointer = self.progPointer
        temp.running = self.running
        temp.turing = self.turing.copy()
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


def solutionPt1(items):
    phase_num = 0
    biggest_out = 0
    biggest_phase = []

    flagged_output = 0

    allComps = []
    for i in range(0, 5):
        allComps.append(Computer(items.copy()))

    possibleSettings = permutations([0,1,2,3,4], 5)

    for setting in possibleSettings:
    # while phase_num < 44444:
    # while phase_num < 3:

        next_buffer = 0
        # phase = digit_splitter(1234, 5)
        phase = setting
        phase_digit = 0
        for amp in allComps:
            amp.reset()
            amp.input = [phase[phase_digit], next_buffer]
            amp.run()
            next_buffer = amp.output[0]
            phase_digit += 1

        if next_buffer > biggest_out:
            print(f"winner: phase {phase_num} : value {next_buffer}")
            biggest_out = next_buffer
            biggest_phase = phase
        # else:
        #     print(f"loser: {next_buffer}")
        if phase_num % 10000 == 0:
            print(f"{int(phase_num/10000)}", end="", flush=True)
            # print("blah")
        # print(phase_num)

        if phase_num == 10432:
            flagged_output = next_buffer

        phase_num += 1

    print(f"tagged output {flagged_output}")

    return biggest_out, biggest_phase


main(parser.parse_args())

