import argparse

parser = argparse.ArgumentParser(description="AoC day 2")
# parser.add_argument("file", help="The file that should be sourced")
parser.add_argument("-p", "--phase", help="The part of the exercise that we are at", type=int, default=1)
parser.add_argument("-t", "--target", help="A target value being aimed for", type=int, default=0)
parser.add_argument("-e", "--endtarget", help="a secondary target", type=int, default=0)


def main(argv):
    print(f"test, {argv}")

    low = argv.target
    high = argv.endtarget

    rules = []

    if argv.phase == 1:
        rules = [increasingRule, containsDoublesRule]
    elif argv.phase == 2:
        rules = [increasingRule, containsOnlyDoublesRule]

    result = ruleRunner(high, low, rules)
    print(len(result))


def digitize(numstr):
    digits = []
    for c in numstr:
        digits.append(int(c))
    return digits

def increasingRule(digits):
    for i in range(0, len(digits)-1):
        if digits[i] > digits[i+1]:
            # print("failed increasing")
            return False
    return True

def containsDoublesRule(digits):
    hasDouble = False
    for i in range(0, len(digits)-1):
        hasDouble = hasDouble or digits[i] == digits[i+1]
    return hasDouble

def containsOnlyDoublesRule(digits):
    hasDouble = False
    lastDigit = digits[0]
    count = 0
    # print(f"--> {digits}")
    for i in range(1, len(digits)):
        # print(f"{lastDigit} -- {digits[i]}")
        if digits[i] == lastDigit:
            count += 1
        elif digits[i] != lastDigit and count == 1:
            hasDouble = True
        else:
            count = 0
        lastDigit = digits[i]
    return hasDouble or count == 1

def ruleRunner(high, low, rules):
    elligible = []
    counter = low
    while counter <= high:
        good = True
        currDigits = digitize(str(counter))
        for rule in rules:
            if not rule(currDigits):
                good = False
                break
        if good:
            elligible.append(counter)
        # else:
        #     print("not good")
        counter += 1

    return elligible


# It is a six-digit number.
# The value is within the range given in your puzzle input.
# Two adjacent digits are the same (like 22 in 122345).
# Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

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

