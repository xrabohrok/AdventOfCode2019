import argparse
import math

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
        for x in item:
            if not x == '\n':
                commands[-1].append(x)

    height = len(commands)
    width = len(commands[0])
    listing = encode_asteroids(commands)
    directory = {}
    for a in listing:
        if not a.pos[0] in directory.keys():
            directory[a.pos[0]] = {}
        directory[a.pos[0]][a.pos[1]] = a

    if argv.phase == 1:
        sol = solutionPt1(directory, listing, height, width)
        for a in listing:
            print(a)
        print(f"winner: {sol}")
    elif argv.phase == 2:
        solutionPt2(directory, listing, height, width, argv.target)


class Asteroid:
    _id = 0

    def __init__(self, x_pos, y_pos):
        self.pos = x_pos, y_pos
        self.checked_by = []
        self.blocked_for = []
        self.id = Asteroid._id
        self.visible = 0
        self.exists = True
        Asteroid._id += 1

    def __str__(self):
        return f"{self.pos[0]}, {self.pos[1]}\t :\t {self.id}: 00 -> {self.visible}"


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

def check_asteroids(source, dest, height, width, directory):
    vec = find_vector(source, dest)
    if vec[0] == 0 and vec[1] == 0:
        return

    unfound = True
    checker = source.pos[0], source.pos[1]
    while 0 <= checker[0] < width and 0 <= checker[1] < height:
        if not (checker[0] == source.pos[0] and checker[1] == source.pos[1]) and checker[0] in directory.keys():
            if checker[1] in directory[checker[0]].keys():
                directory[checker[0]][checker[1]].checked_by.append(source.id)
                if unfound:
                    source.visible += 1
                    unfound = False
                else:
                    directory[checker[0]][checker[1]].blocked_for.append(source.id)
        checker = checker[0] + vec[0], checker[1] + vec[1]


def check_all_asteroids(listing, directory, width, height):
    for a in listing:
        for b in listing:
            if not a == b and a.id not in b.checked_by:
                check_asteroids(a, b, height, width, directory)


def angle_asteroids(listing, x, y):
    orig = x, y
    angles = {}
    for a in listing:
        if a.pos[0] == x and a.pos[1] == y:
            continue
        angle = math.atan2(a.pos[1] - orig[1], a.pos[0] - orig[0]) + math.pi / 2

        # normalize
        if angle < 0:
            angle += 2 * math.pi
        distance = math.dist(orig, a.pos)
        angle_index = int(angle * 100000)
        if angle_index not in angles.keys():
            angles[angle_index] = []
        angles[angle_index].append((a, distance, angle))

    for entry in angles.keys():
        angles[entry].sort(key=lambda d: d[1])

    return angles

def vaporize_problems(angled_rocks, angle_order, count):
    vaporized_set = []
    vaporized_count = 0
    while vaporized_count < count:
        for angle in angle_order:
            for rock in angled_rocks[angle]:
                if rock[0].exists:
                    print(f"xx - {vaporized_count}:: {rock[0].pos} -- {rock[2] * 180 / math.pi}")
                    rock[0].exists = False
                    vaporized_set.append(rock[0])
                    vaporized_count += 1
                    break
    print(angled_rocks[angle_order[0]])
    return vaporized_set

def solutionPt1(asteroid_dict, asteroid_list, height, width):
    check_all_asteroids(asteroid_list, asteroid_dict, height, width)
    asteroid_list.sort(key=lambda a: a.visible)
    return asteroid_list[-1]

def solutionPt2(asteroid_dict, asteroid_list, height, width, target):
    winner = solutionPt1(asteroid_dict, asteroid_list, height, width)
    angles = angle_asteroids(asteroid_list, winner.pos[0], winner.pos[1])

    order = []
    for o in angles.keys():
        order.append(o)
    order.sort()

    # for o in order:
    #     print(f"{angles[o][0][0]} -- {angles[o][0][2] * 180 / math.pi}")
    # print("=========")

    death_list = vaporize_problems(angles, order, len(asteroid_list)-1)

    # for o in death_list:
    #     print(o)

    bet = death_list[target]
    compute = bet.pos[0] * 100 + bet.pos[1]
    print(f"{target} vaporized is {bet.pos} which computes to {compute}")



main(parser.parse_args())

