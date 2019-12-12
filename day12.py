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
        commands.append({})

        item = item.strip('<>\n')
        numSet = str.split(item, ',')
        for block in numSet:
            block = block.split('=')
            block2 = list(map(lambda x: x.strip(' \n'), block))
            commands[-1][block2[0]] = block2[1]

    moons = []
    for c in commands:
        moons.append(Moon(int(c["x"]), int(c["y"]), int(c["z"])))

    if argv.phase == 1:
        sol = solutionPt1(moons, argv.target)
        print(f"The total energy is {sol}")
    elif argv.phase == 2:
        sol = solutionPt2(moons)
        print(f"The repeat is at{sol}")


class Moon:
    id = 0

    def __init__(self, x, y, z):
        self.id = Moon.id
        self.pos = x, y, z
        self.vel = 0, 0, 0
        self.vel1 = 0
        self.energy = 0

        self.checked_with = []
        Moon.id += 1

    def add_gravity(self, other_moon):
        
        change = [0, 0, 0]
        for iter in range(0, 3):
            if self.pos[iter] > other_moon.pos[iter]:
                change[iter] = -1
            elif self.pos[iter] < other_moon.pos[iter]:
                change[iter] = 1

        self.vel = self.vel[0] + change[0], self.vel[1] + change[1], self.vel[2] + change[2]
        other_moon.vel = other_moon.vel[0] - change[0], other_moon.vel[1] - change[1], other_moon.vel[2] - change[2]

        self.checked_with.append(other_moon.id)
        other_moon.checked_with.append(self.id)


    def reset_checked_by(self):
        self.checked_with = []

    def apply_velocity(self):
        self.pos = self.vel[0] + self.pos[0], self.vel[1] + self.pos[1], self.vel[2] + self.pos[2]

    def find_energy(self):
        potential = 0
        for i in self.pos:
            potential += abs(i)
        kinetic = 0
        for i in self.vel:
            kinetic += abs(i)
        self.energy = kinetic * potential

        return self.energy

    def __str__(self):
        return f"<pos id={self.id} x={self.pos[0]}, y={self.pos[1]}, z={self.pos[2]}>" \
            f"<vel x={self.vel[0]}, y={self.vel[1]}, z={self.vel[2]}>"

    def state_hash(self):
        thing = self.pos[0]
        return f"{thing}"


# To apply gravity, consider every pair of moons. On each axis (x, y, and z),
# the velocity of each moon changes by exactly +1 or -1 to pull the moons together.
# For example, if Ganymede has an x position of 3, and Callisto has a x position of 5,
# then Ganymede's x velocity changes by +1 (because 5 > 3) and
# Callisto's x velocity changes by -1 (because 3 < 5).
# However, if the positions on a given axis are the same,
# the velocity on that axis does not change for that pair of moons.

# Once all gravity has been applied, apply velocity:
# simply add the velocity of each moon to its own position.

#Then, it might help to calculate the total energy in the system.
# The total energy for a single moon is its potential energy multiplied by its kinetic energy.
# A moon's potential energy is the sum of the absolute values of its x, y, and z position coordinates.
# A moon's kinetic energy is the sum of the absolute values of its velocity coordinates.

def solutionPt1(moons, target_cycle):

    cycle = 0
    while cycle < target_cycle:
        for m in moons:
            for m2 in moons:
                if m.id not in m2.checked_with and not m.id == m2.id:
                    m.add_gravity(m2)

        for m in moons:
            m.apply_velocity()
            m.reset_checked_by()
        cycle += 1

    energy = sum(m.find_energy() for m in moons)

    for p in moons:
        print(p)

    return energy

def solutionPt2(moons):
    # tree


main(parser.parse_args())