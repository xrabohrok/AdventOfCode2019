import argparse

parser = argparse.ArgumentParser(description="AoC day 4")
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


main(parser.parse_args())

