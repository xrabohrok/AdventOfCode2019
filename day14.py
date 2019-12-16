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
    rules = []
    for item in allItems:
        numSet = str.split(item, "=>")
        result = numSet[1]
        ingredients = numSet[0].split(",")
        result_parts = result.strip().split(' ')
        cur_rule = Rule(result_parts[1].strip(' '), int(result_parts[0].strip(' ')))
        for x in ingredients:
            ingredient_part = x.strip().split(' ')
            cur_rule.add_ingredient(ingredient_part[1].strip(' '), int(ingredient_part[0].strip(' ')))
        rules.append(cur_rule)

    if argv.phase == 1:
        sol = solutionPt1(rules, "ORE", "FUEL")
        print(f"The memory dump is {sol}")
    # elif argv.phase == 2:
    #     sol = solutionPt2(commands, argv.target)
    #     print(f"The correct inputs are {sol}")

def solutionPt1(rules, raw, target):
    lookup = {}

    # add rule for raw because it will not be provided
    rules.append(Rule(raw, 1))
    for r in rules:
        lookup[r.name] = r

    root = Node(None, 1, lookup[target])
    all_nodes = [root]
    stack = [root]

    while len(stack) > 0:
        # done, go up
        if stack[-1].is_done() or stack[-1].rule.name == raw:
            stack.pop()
        # dive!
        else:
            next_rule_name = stack[-1].rule.ingredient_names[len(stack[-1].children)]
            dive_rule = lookup[next_rule_name]

            runs = 1
            # keep running the rule until it meets needs
            # probably a better way to do this, involving int cieling
            # need to add a "bank" concept
            needed = stack[-1].rule.ingredients[next_rule_name] * stack[-1].mult
            next_rule_output = lookup[next_rule_name].result_amt
            while runs * next_rule_output < needed:
                runs += 1

            next_node = Node(stack[-1], runs, dive_rule)
            stack[-1].children.append(next_node)
            stack.append(next_node)
            all_nodes.append(next_node)

    raw_mats = 0
    for n in all_nodes:
        if n.rule.name == raw:
            raw_mats += n.mult

    return raw_mats



    #find the root rule

class Rule:
    def __init__(self, result_name, result_num):
        self.name = result_name
        self.result_amt = result_num
        self.ingredients = {}
        self.ingredient_names = []

    def add_ingredient(self, input, amount=1):
        self.ingredients[input] = amount
        self.ingredient_names.append(input)

    def __str__(self):
        return f"=={self.name}"

class Node:
    def __init__(self, parent, multiplier, rule):
        self.parent = parent
        self.mult = multiplier
        self.rule = rule
        self.children = []

    def is_done(self):
        return len(self.children) == len(self.rule.ingredients.keys())

    def __str__(self):
        return f"({self.rule.name}) x {self.mult}"


main(parser.parse_args())

