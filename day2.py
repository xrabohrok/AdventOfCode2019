import argparse

parser = argparse.ArgumentParser(description="AoC day 2")
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
        print(f"The memory dump is {sol}")
    elif argv.phase == 2:
        sol = solutionPt2(commands, argv.target)
        print(f"The correct inputs are {sol}")


# Opcode 1 adds together numbers read from two positions and stores the result in a third position.
# The three integers immediately after the opcode tell you these three positions
# - the first two indicate the positions from which you should read the input values,
# and the third indicates the position at which the output should be stored.

# Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them.
# Again, the three integers after the opcode indicate where the inputs and outputs are, not their values.

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


def parseCodes(curState):
    opd = curState.clone()
    # print(f"pointer at{curState.progPointer}")
    # print(f"program is {curState.turing}")
    if curState.turing[curState.progPointer] == 1:
        # Add from first two positions, store in the third
        opd.turing[opd.turing[opd.progPointer + 3]] = opd.turing[opd.turing[opd.progPointer+1]] + opd.turing[opd.turing[opd.progPointer+2]]
        opd.progPointer += 4
    elif curState.turing[curState.progPointer] == 2:
        # Add from first two positions, store in the third
        opd.turing[opd.turing[opd.progPointer + 3]] = opd.turing[opd.turing[opd.progPointer+1]] * opd.turing[opd.turing[opd.progPointer+2]]
        opd.progPointer += 4
    elif curState.turing[curState.progPointer] == 99:
        # halt
        opd.running = False
    else:
        #error
        opd.running = False
        opd.errored = True

    return opd


def solutionPt1(items):
    program = progState()
    program.turing = items
    while program.running :
        program = parseCodes(program)
        if program.errored:
            print(f"irregular execution at pointer {program.progPointer}")

    return program.turing

def solutionPt2(items, target):

    initState = progState()
    initState.turing = items
    for x in range(0, 99):
        for y in range(0, 99):
            program = initState.clone()
            program.turing[1] = x
            program.turing[2] = y
            # print(f"{x}, {y}")
            while program.running:
                program = parseCodes(program)
                if program.errored:
                    print(f"irregular execution at pointer {program.progPointer}")
            if program.turing[0] == target:
                print(f"target found: {x}, {y}")
                return x, y

    return None


main(parser.parse_args())

