import argparse

parser = argparse.ArgumentParser(description="AoC day 10")
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

    commands = []
    for item in allItems:
        commands.append([])
        numSet = str.split(item, ',')
        for x in numSet:
            commands[-1].append(x)

    height = len(commands)
    width = len(commands[0])
    field = encode_asteroids(commands)
    listing = {}
    for a in field:
        if not a.pos[0] in listing.keys():
            listing[a.pos[0]] = {}
        listing[a.pos[0]][a.pos[1]] = a



    # if argv.phase == 1:
    #     sol = solutionPt1(commands)
    #     print(f"The memory dump is {sol}")
    # elif argv.phase == 2:
    #     sol = solutionPt2(commands, argv.target)
    #     print(f"The correct inputs are {sol}")


class Asteroid:
    _id = 0

    def __init__(self, x_pos, y_pos):
        self.pos = x_pos, y_pos
        self.checked_by = []
        self.blocked_for = []
        self.id = Asteroid._id
        self.visible = 0
        Asteroid._id += 1

    def __str__(self):
        return f"{self.pos[0]}, {self.pos[1]} : {self.id}"


def encode_asteroids(commands):
    y = 0
    asteroids = []
    for j in commands:
        x = 0
        for i in j:
            if i == '#':
                asteroids.append(Asteroid(x, y))
            x += 1
        y += 1
    return asteroids

def computeGCD(x, y):
    while y:
        x, y = y, x % y
    return x

def find_vector(asteroid_a, asteroid_b):
    vec = asteroid_b.pos[0] - asteroid_a.pos[0],  asteroid_b.pos[1] - asteroid_a.pos[1]
    gcd = computeGCD(abs(vec[0]), abs(vec[1]))
    if gcd > 1:
        vec = vec[0]/gcd, vec[1]/gcd
    return vec

def check_asteroids(source, dest, height, width, listing):
    vec = find_vector(source, dest)
    if vec[0] == 0 and vec[1] == 0:
        return

    unfound = True
    checker = source.pos[0], source.pos[1]
    while 0 <= checker[0] < width and 0 <= checker[1] < height:
        if not checker[0] == source.pos[0] and not checker[1] == source.pos[1] and checker[0] in listing.keys and checker[1] in listing[checker[0]].keys:
            listing[checker[0]][checker[1]].checked_by = source.id
            if unfound:
                source.visible += 1
                unfound = False
            else:
                listing[checker[0]][checker[1]].blocked_for = source.id
        checker = checker[0] + vec[0], checker[1] + vec[1]

def check_all_asteroids(asteroids, listing, width, height):
    for a in asteroids:
        for b in asteroids:
            if not a == b:
                check_asteroids(a, b, height, width, listing)




def solutionPt1(items):
    None

def solutionPt2(items, target):
    None


main(parser.parse_args())

