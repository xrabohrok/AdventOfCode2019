
import argparse

parser = argparse.ArgumentParser(description="AoC day x")
parser.add_argument("file", help="The file that should be sourced")
parser.add_argument("-p", "--phase", help="The part of the exercise that we are at", type=int, default=1)


def main(argv):
    print(f"test, {argv}")

    infile = open(argv.file, "r")

    for line in infile:
        #do a line operation
        if line:
            print(line)

    infile.close()



main(parser.parse_args())

