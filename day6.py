import argparse

parser = argparse.ArgumentParser(description="AoC day 6")
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
    betterCommands = processCommands(allItems)
    tree = buildTree(betterCommands)
    # for name in tree.keys():
    #     print(f"{tree[name]}")

    if argv.phase == 1:
        sol = solutionPt1(tree)
        print(f"The total number of orbits is {sol}")
    elif argv.phase == 2:
        sol = solutionPt2(tree)
        print(f"The min number of orbital transfers is: {len(sol) - 3}")


class Planet:

    def __init__(self, name):
        self.name = name
        self.children = []
        self.searched = False
        self.parent = None

    def addChild(self, child):
        self.children.append(child)
        if child.parent is not None:
            print(f"something is wrong with parent {self.name} and child {child.name}")
        else:
            child.parent = self

    def __str__(self):
        str = f"+ {self.name} ++++++++++++++++++"

        if self.parent is not None:
            str += f"\nParent: {self.parent.name}"

        if len(self.children) == 0:
            str += "\n=== LEAF ==="
        elif len(self.children) > 0:
            for child in self.children:
                str += f"\n--- {child.name}"
        elif self.parent is None:
            str += "\n========== ROOT ============="
        return str


def processCommands(commands):
    splitCommands = []
    for command in commands:
        commandSet = str.split(command, ')')
        commandSet[1] = commandSet[1].strip('\n')
        splitCommands.append(commandSet)
    return splitCommands

def buildTree(commands):
    allPlanets = {}
    # root ) child
    for command in commands:
        if not command[0] in allPlanets.keys():
            allPlanets[command[0]] = Planet(command[0])
        if not command[1] in allPlanets.keys():
            allPlanets[command[1]] = Planet(command[1])

        allPlanets[command[0]].addChild(allPlanets[command[1]])
    return allPlanets


def solutionPt1(planetTree):
    jumps = 0
    for planet in planetTree.keys():
        #count jumps for each planet
        cur_planet = planetTree[planet]
        while cur_planet.parent is not None:
            jumps += 1
            cur_planet = cur_planet.parent

    return jumps

def solutionPt2(planetTree):
    stack = [planetTree["YOU"]]

    temp = planetTree["YOU"]

    while stack[-1] != planetTree["SAN"]:
        cur = stack[-1]

        # all = []
        # for i in stack:
        #     all.append(i.name)
        # print(all)

        #done with children, go up tree
        nextUnsearched = None
        if len(cur.children) > 0:
            nextUnsearched = next((i for i in cur.children if not i.searched), None)
        if nextUnsearched is None:
            # we started low and are still going up
            if len(stack) == 1 or cur.parent != stack[-2]:
                cur.searched = True
                stack.append(cur.parent)
                continue
            #backtracking
            elif cur.parent == stack[-2]:
                cur.searched = True
                stack.pop()
                continue

        # dive!
        stack.append(nextUnsearched)

    return stack


main(parser.parse_args())

