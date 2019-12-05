import argparse

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
        print("All outputs should be zero")
        sol = solutionPt1(commands)


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

def getModes(number):
    return int(int(number % 1000 / 100)), int(number % 10000 / 1000), int(number / 10000)

def getOp(number):
    return int(number % 100)

def parseCodes(curState):
    opd = curState.clone()
    command = getOp(curState.turing[curState.progPointer])
    # mode 0 positional, 1 immediate
    mode = getModes(curState.turing[curState.progPointer])

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
        # take keyboard input
        print("HALT---AWAITING INPUT:")
        opd.turing[opd.turing[opd.progPointer + 1]] = int(input())
        opd.progPointer += 2
    elif command == 4:
        # output to screen
        print(paramA)
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
        print("--FINISH--")
    else:
        #error
        opd.running = False
        opd.errored = True

    return opd


def solutionPt1(items):
    program = progState()
    program.turing = items
    while program.running:
        program = parseCodes(program)
        if program.errored:
            print(f"irregular execution at pointer {program.progPointer}")

    return program.turing



main(parser.parse_args())

