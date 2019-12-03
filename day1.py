import argparse

parser = argparse.ArgumentParser(description="AoC day x")
parser.add_argument("file", help="The file that should be sourced")
parser.add_argument("-p", "--phase", help="The part of the exercise that we are at", type=int, default=1)


def main(argv):
    print(f"test, {argv}")

    infile = open(argv.file, "r")

    allItems = []

    for line in infile:
        # do a line operation
        if line:
            allItems.append(int(line))

    infile.close()

    if argv.phase == 1:
        sol = solutionPt1(allItems)
        print(f"The target mass is {sol}")
    elif argv.phase == 2:
        sol = solutionPt2(allItems)
        print(f"The fuel adjusted fuel weight is now {sol}")


# Fuel required to launch a given module is based on its mass.
# Specifically, to find the fuel required for a module, take its mass,
# divide by three, round down, and subtract 2.


def solutionPt1(items):
    sum = 0
    for item in items:
        sum += int(item / 3) - 2

    return sum


def solutionPt2(items):
    sum = 0
    for item in items:
        tumbler = int(item / 3) - 2
        while tumbler > 0:
            sum += tumbler
            tumbler = int(tumbler / 3) - 2

    return sum


main(parser.parse_args())

