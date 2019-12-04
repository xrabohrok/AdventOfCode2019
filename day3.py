import argparse

parser = argparse.ArgumentParser(description="AoC day 3")
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
        commands.append(numSet)


    if argv.phase == 1:
        sol = solutionPt1(commands)
        print(f"The shortest point is {sol}")
    elif argv.phase == 2:
        sol = solutionPt2(commands)
        print(f"The closest point in terms of propagation delay is {sol}")

def processCommands(commands):
    betterCommands = []
    for commandSet in commands:
        betterCommands.append([])
        for command in commandSet:
            # print(command)
            betterCommands[-1].append((command[0], int(command[1:])))
    return betterCommands

# find the bounding grid for these wires
def findzerozerobounds(lines):
    upperVertical = 0
    lowerVertical = 0
    upperHorizontal = 0
    lowerHorizontal = 0
    ends = []
    for line in lines:
        pos = 0, 0
        for command in line:
            if command[0] == 'R':
                pos = pos[0] + command[1], pos[1]
                if pos[0] > upperHorizontal:
                    upperHorizontal = pos[0]
            elif command[0] == 'L':
                pos = pos[0] - command[1], pos[1]
                if pos[0] < lowerHorizontal:
                    lowerHorizontal = pos[0]
            elif command[0] == 'U':
                pos = pos[0], pos[1] + command[1]
                if pos[1] > upperVertical:
                    upperVertical = pos[1]
            elif command[0] == 'D':
                pos = pos[0], pos[1] - command[1]
                if pos[1] < lowerVertical:
                    lowerVertical = pos[1]
    return upperHorizontal, lowerHorizontal, upperVertical, lowerVertical

# setup the sandbox
def buildGrid(bounds):
    grid = []
    for i in range(0, bounds[0] + abs(bounds[1])+1):
        grid.append([])
        for j in range(0, bounds[2] + abs(bounds[3])+1):
            grid[-1].append("")
    print("done gridding")
    return grid

def drawSegment(grid, horizInc, vertInc, pos, id, amount, distance):
    distTraveledVert = 0
    distTraveledHoriz = 0
    intersections = []
    while distTraveledHoriz < amount and distTraveledVert < amount:
        # print(f"pos {pos}")
        # print(f"grid {len(grid)}, {len(grid[0])}")
        curSpot = grid[pos[0]][pos[1]]
        # if len(curSpot) > 0:
        #     print(f"peek {curSpot}")
        distance +=1
        if len(curSpot) >= 1 and str.find(curSpot, f"id:{id}") == -1:
            intersections.append(pos)
        grid[pos[0]][pos[1]] += f"^id:{id}|{distance}|"
        pos = pos[0] + horizInc, pos[1] + vertInc
        distTraveledVert += abs(vertInc)
        distTraveledHoriz += abs(horizInc)
    return pos, grid, intersections, distance

def traceAndIntercept(grid, wirecommands, bounds, id):
    pos = abs(bounds[1]), abs(bounds[3])
    intersections = []
    distance = 0
    for command in wirecommands:
        # print(f"bounds {bounds}")
        # print(f"command {command}")
        if command[0] == 'U':
            result = drawSegment(grid, 0, 1, pos, id, command[1], distance)
            pos = result[0]
            grid = result[1]
            intersections += result[2]
            distance = result[3]
        elif command[0] == 'D':
            result = drawSegment(grid, 0, -1, pos, id, command[1], distance)
            pos = result[0]
            grid = result[1]
            intersections += result[2]
            distance = result[3]
        elif command[0] == 'L':
            result = drawSegment(grid, -1, 0, pos, id, command[1], distance)
            pos = result[0]
            grid = result[1]
            intersections += result[2]
            distance = result[3]
        elif command[0] == 'R':
            result = drawSegment(grid, 1, 0, pos, id, command[1], distance)
            pos = result[0]
            grid = result[1]
            intersections += result[2]
            distance = result[3]

    return intersections

def manhattanDist(pointa, pointb):
    return abs(pointa[0] - pointb[0]) + abs(pointa[1] - pointb[1])

def stepsFromPoint(point, grid):
    sum = 0
    sections = str.split(grid[point[0]][point[1]], '|')
    for section in sections:
        if str.find(section, "id") == -1 and str.isnumeric(section):
            sum += int(section)
    # subtract the two starting squares
    return sum - 2

def solutionPt1(items):
    commands = processCommands(items)
    print(f"command sets: {len(commands)}")
    bounds = findzerozerobounds(commands)
    print(f"bounds: {bounds}")
    grid = buildGrid(bounds)

    # center = int((bounds[0] + abs(bounds[1])/2)), int((bounds[2] + abs(bounds[3])/2))
    center = abs(bounds[1]), abs(bounds[3])

    results = []
    for idx, cmdset in enumerate(commands):
        print(f"line {idx}")
        results += traceAndIntercept(grid, cmdset, bounds, idx)

    # print(results)
    distIntersections = []
    for intersection in results:
        distIntersections.append((manhattanDist(center, intersection), intersection))
    distIntersections.sort()

    return distIntersections[1]


def solutionPt2(items):
    commands = processCommands(items)
    print(f"command sets: {len(commands)}")
    bounds = findzerozerobounds(commands)
    print(f"bounds: {bounds}")
    grid = buildGrid(bounds)

    # center = int((bounds[0] + abs(bounds[1])/2)), int((bounds[2] + abs(bounds[3])/2))
    center = abs(bounds[1]), abs(bounds[3])

    results = []
    for idx, cmdset in enumerate(commands):
        print(f"line {idx}")
        results += traceAndIntercept(grid, cmdset, bounds, idx)

    # print(results)
    distIntersections = []
    for intersection in results:
        distIntersections.append((stepsFromPoint(intersection, grid), intersection))
        #print(f"{grid[intersection[0]][intersection[1]]}")
    distIntersections.sort()
    #print(distIntersections)

    # counting the squares entered, not total squares, remove the two starters
    return distIntersections[1]


main(parser.parse_args())

