import argparse
import os
import enum
from itertools import permutations
parser = argparse.ArgumentParser(description="AoC day 15")
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
        print(f"Total was {sol[0]}")
    elif argv.phase == 2:
        sol = solutionPt2(commands)
        print(f"Final score: {sol}")


def solutionPt2(commands):
    whatev, world, final = solutionPt1(commands)
    minutes = 1
    world.tree[final[1]][final[0]].has_oxygen = True
    world.tree[final[1]][final[0]].oxygenated_on = 0
    fronts = world.tree[final[1]][final[0]].neighbors.copy()

    while len(fronts) > 0:
        new_fronts = []
        for f in fronts:
            thing = world.tree[f[1]][f[0]]
            thing.has_oxygen = True
            for n in thing.neighbors:
                other_thing = world.tree[n[1]][n[0]]
                if not other_thing.has_oxygen:
                    new_fronts.append(n)
        fronts = new_fronts
        minutes += 1
        world.draw((0, 0))

    return minutes


def solutionPt1(commands):
    world = Graph()
    world.add_node(0,0, NodeType.floor)
    pos = 0, 0
    final = None

    drone = Computer(commands, halting_output=True)

    while len(world.unsearched) > 0:
        target = world.unsearched[-1]
        path = world.a_star(target[0], target[1], pos[0], pos[1])
        path.remove(pos)
        for step in path:
            move = step[0] - pos[0], step[1] - pos[1]
            command = 0
            if move[0] == -1:
                command = 3
            elif move[0] == 1:
                command = 4
            elif move[1] == 1:
                command = 1
            elif move[1] == -1:
                command = 2

            #try move
            drone.insert_pipeline(command)
            drone.run(restart=False)
            result = drone.read_pipeline()

            if result == 0:
                world.add_node(step[0], step[1], NodeType.wall)
                break
            elif result == 1:
                world.add_node(step[0], step[1], NodeType.floor)
                pos = step
            elif result == 2:
                world.add_node(step[0], step[1], NodeType.leak)
                pos = step
                final = step
        world.draw(pos)

    final_path = world.a_star(final[0], final[1], 0, 0)
    return len(final_path) - 1, world, final



class NodeType(enum.Enum):
    wall = 0
    floor = 1
    leak = 2
    unsearched = 3


class Graph:
    def __init__(self):
        self.tree = {}
        self.unsearched = []

    def seen_node(self, x, y):
        return y in self.tree.keys() and x in self.tree[y].keys()

    def add_node(self, x, y, node_type):
        if self.seen_node(x, y):
            return

        if y not in self.tree.keys():
            self.tree[y] = {}
        if x not in self.tree[y].keys():
            self.tree[y][x] = Node(x, y, node_type)
            if (x,y) in self.unsearched:
                self.unsearched.remove((x, y))

        # because walls are dead ends, they don't spiral out the way others do
        radial = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        if node_type != NodeType.wall:
            for r in radial:
                suspect = r[0] + x, r[1] + y
                # untouched and unmapped
                if suspect not in self.unsearched and (suspect[1] not in self.tree.keys() or suspect[0] not in self.tree[suspect[1]].keys()):
                    self.unsearched.append(suspect)
                    for n in radial:
                        possible = n[0] + x, n[1] + y
                        if not self.seen_node(possible[0], possible[1]) or self.tree[possible[1]][possible[0]].node_type != NodeType.wall:
                            if suspect not in self.tree[y][x].neighbors:
                                self.tree[y][x].neighbors.append(suspect)
                # mapped, but untouched
                elif suspect not in self.unsearched:
                    node_checked = self.tree[suspect[1]][suspect[0]]
                    if node_checked.node_type == NodeType.floor or node_checked.node_type == NodeType.leak:
                        if (x, y) not in node_checked.neighbors:
                            node_checked.neighbors.append((x, y))
                        if (x, y) not in self.tree[y][x].neighbors:
                            self.tree[y][x].neighbors.append(suspect)
        else:
            # walls are not legitimate a star nodes and must be removed
            for r in radial:
                suspect = r[0] + x, r[1] + y
                if self.seen_node(suspect[0], suspect[1]):
                    if (x, y) in self.tree[suspect[1]][suspect[0]].neighbors:
                        self.tree[suspect[1]][suspect[0]].neighbors.remove((x, y))

    def heuristic(self, there, here):
        return abs(there[0] - here[0]) + abs(there[1] - here[1])

    def a_star(self, target_x, target_y, start_x, start_y):
        searched = [SearchNode(start_x, start_y, 0, 1, None)]
        target = target_x, target_y
        unsearched = []
        start_neighbors = self.tree[start_y][start_x].neighbors
        for i in range(0, len(start_neighbors)):
            newNode = SearchNode(start_neighbors[i][0], start_neighbors[i][1], self.heuristic(target, start_neighbors[i]), 1, searched[0])
            unsearched.append(newNode)
        while searched[-1].pos != target and len(unsearched) > 0:
            unsearched.sort(key=lambda x: x.value + x.steps)
            cur = unsearched[0]
            unsearched.remove(cur)
            searched.append(cur)
            if not self.seen_node(cur.pos[0], cur.pos[1]) and cur.pos == target:
                # we are trying for an unknown end tile, call it a day
                break
            elif not self.seen_node(cur.pos[0], cur.pos[1]):
                # no further processing on missing nodes, not to be considered for thru pathing
                continue
            cur_node = self.tree[cur.pos[1]][cur.pos[0]]
            steps = cur.steps + 1
            for i in cur_node.neighbors:
                if next((n for n in unsearched if n.pos == i), -1) == -1 and next((n for n in searched if n.pos == i), -1) == -1:
                    new_node = SearchNode(i[0], i[1], self.heuristic(cur.pos, target), steps, cur)
                    unsearched.append(new_node)
        path = [searched[-1]]
        while path[-1].parent is not None:
            path.append(path[-1].parent)

        path.reverse()
        list_path = [x.pos for x in path]
        return list_path

    def draw(self, tracer):
        ymax = max(self.tree.keys())
        ymin = min(self.tree.keys())
        xmax = 30
        xmin = -30

        sprite = ['#','.', 'X', '.']

        os.system("cls")

        for j in range(ymin, ymax+1):
            for i in range(xmin, xmax):
                if (i, j) == tracer:
                    print("0", end='', flush=False)
                elif self.seen_node(i, j):
                    if self.tree[j][i].has_oxygen:
                        char = '3'
                    else:
                        char = sprite[self.tree[j][i].node_type.value]
                    print(char, end='', flush=False)
                else:
                    print(' ', end='', flush=False)
            print()


class SearchNode:
    def __init__(self, x, y, value, steps, prev):
        self.pos = x, y
        self.parent = prev
        self.value = value
        self.steps = steps

    def __str__(self):
        return f"({self.pos})"

class Node:
    def __init__(self, x, y, node_type = NodeType.unsearched):
        self.pos = x, y
        self.node_type = node_type
        self.neighbors = []
        self.has_oxygen = False
        self.oxygenated_on = -1

    def __str__(self):
        return f"{len(self.neighbors)} -> ({self.pos})"


##############################################################
##################### NO TOUCH ###############################

class Computer:
    def __init__(self, program, prog_input=None, halting_output=False):
        self.program_orig = program
        self.output = []
        self.halting_output = halting_output

        self.inpipe = []
        self.outpipe = []
        self.cur_state = None

    def reset(self):
        self.output = []
        self.input = [None]
        self.cur_state = None
        # for i in range(0, len(self.program_orig)):
        #     self.program[i] = self.program_orig[i]

    def run(self, restart=True):
        if self.cur_state is None or restart:
            self.cur_state = progState()
            self.cur_state.turing = self.program_orig

        if self.cur_state.paused_for_stream:
            self.cur_state.paused_for_stream = False

        while self.cur_state.running:
            self.cur_state = self._parseCodes(self.cur_state)
            if self.cur_state.errored:
                print(f"irregular execution at pointer {self.cur_state.progPointer}")
            if self.cur_state.paused_for_input or self.cur_state.paused_for_stream:
                return self.cur_state.turing

        return self.cur_state.turing

    def is_running(self):
        if self.cur_state is None:
            return False
        return self.cur_state.running

    def insert_pipeline(self, thing):
        self.inpipe = [int(thing)]

    def read_pipeline(self):
        if len(self.outpipe) > 0:
            # print(f" popped {self.outpipe[-1]}")
            return self.outpipe.pop()
        else:
            return None

    def _getModes(self, number):
        return int(int(number % 1000 / 100)), int(number % 10000 / 1000), int(number / 10000)

    def _getOp(self, number):
        return int(number % 100)

    def _grow_mem(self, state, spot):
        if spot >= len(state.turing):
            growth = spot - len(state.turing)
            for i in range(0, growth+2):
                state.turing.append(0)
        return state


    def _parseCodes(self, curState):
        opd = curState.clone()
        command = self._getOp(curState.turing[curState.progPointer])
        # mode 0 positional, 1 immediate
        mode = self._getModes(curState.turing[curState.progPointer])

        # print(f"pointer at {curState.progPointer}")
        # print(f"command is {command}")
        # print(f"mode is {mode}")
        # print(f"program is {curState.turing}")

        # 0 address mode
        # 1 immediate mode
        # 2 relative (offset) mode
        loc = 0
        if command in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if mode[0] == 0:
                loc = opd.turing[opd.progPointer + 1]
            elif mode[0] == 1:
                loc = opd.progPointer + 1
            elif mode[0] == 2:
                loc = opd.relative_base + opd.turing[opd.progPointer + 1]
            opd = self._grow_mem(opd, loc)
            paramA = opd.turing[loc]
        paramA_loc = loc

        loc = 0
        if command in [1, 2, 5, 6, 7, 8]:
            if mode[1] == 0:
                loc = opd.turing[opd.progPointer + 2]
            elif mode[1] == 1:
                loc = opd.progPointer + 2
            elif mode[1] == 2:
                loc = opd.relative_base + opd.turing[opd.progPointer + 2]
            opd = self._grow_mem(opd, loc)
            paramB = opd.turing[loc]
        paramB_loc = loc

        loc = 0
        if command in [1, 2, 7, 8]:
            if mode[2] == 0:
                loc = opd.turing[opd.progPointer + 3]
            elif mode[2] == 1:
                opd.errored = True
                opd.running = False
                print("Illegal write mode *immediate*")
                return opd
            elif mode[2] == 2:
                loc = opd.relative_base + opd.turing[opd.progPointer + 3]
            opd = self._grow_mem(opd, loc)
        paramC_loc = loc

        if command == 1:
            # Add from first two positions, store in the third
            opd.turing[paramC_loc] = paramA + paramB
            opd.progPointer += 4
        elif command == 2:
            # Add from first two positions, store in the third
            opd.turing[paramC_loc] = paramA * paramB
            opd.progPointer += 4
        elif command == 3:
            # take input
            if opd.paused_for_input:
                opd.turing[paramA_loc] = self.inpipe.pop()
                opd.paused_for_input = False
            else:
                if len(self.inpipe) == 1:
                    opd.turing[paramA_loc] = self.inpipe.pop()
                    opd.paused_for_input = False
                else:
                    opd.paused_for_input = True
                    return opd
            opd.progPointer += 2
        elif command == 4:
            # output to buffer
            self.outpipe.insert(0, paramA)
            opd.progPointer += 2
            if self.halting_output:
                opd.paused_for_stream = True
                return opd
        elif command == 5:
            # first value not zero, set pointer to second val
            opd.progPointer = paramB if paramA != 0 else opd.progPointer + 3
        elif command == 6:
            # first value zero, set pointer to second val
            opd.progPointer = paramB if paramA == 0 else opd.progPointer + 3
        elif command == 7:
            # if first param is less than second, store 1 in third, otherwise 0
            opd.turing[paramC_loc] = 1 if paramA < paramB else 0
            opd.progPointer += 4
        elif command == 8:
            # if first param is equal to second, store 1 in third, otherwise 0
            opd.turing[paramC_loc] = 1 if paramA == paramB else 0
            opd.progPointer += 4
        elif command == 9:
            # add to the prog's relative base
            opd.relative_base += paramA
            opd.progPointer += 2
        elif command == 99:
            # halt
            opd.running = False
            # print("--FINISH--")
        else:
            # error
            opd.running = False
            opd.errored = True

        return opd


class progState:
    def __init__(self):
        self.progPointer = 0
        self.turing = []
        self.running = True
        self.errored = False
        self.paused_for_input = False
        self.paused_for_stream = False
        self.relative_base = 0

    def clone(self):
        temp = progState()
        temp.progPointer = self.progPointer
        temp.running = self.running
        temp.turing = self.turing.copy()
        temp.paused_for_input = self.paused_for_input
        temp.paused_for_stream = self.paused_for_stream
        temp.relative_base = self.relative_base
        return temp


def digit_splitter(num, min_size=1):
    sign = 1
    digits = []
    if num < 0:
        sign = -1
        num = abs(num)
    place = 1
    while num > place:
        digits.append(int(num % (place * 10) / place) * sign)
        place *= 10

    while len(digits) < min_size:
        digits.append(0)
    digits.reverse()
    return digits

##################### NO TOUCH ###############################
##############################################################

main(parser.parse_args())