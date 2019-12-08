import argparse

parser = argparse.ArgumentParser(description="AoC day 8")
parser.add_argument("file", help="The file that should be sourced")
parser.add_argument("-p", "--phase", help="The part of the exercise that we are at", type=int, default=1)
parser.add_argument("-w", "--width", help="width of image", type=int, default=1)
parser.add_argument("-t", "--height", help="height of image", type=int, default=1)


def main(argv):
    print(f"test, {argv}")

    infile = open(argv.file, "r")

    allItems = []

    for line in infile:
        # do a line operation
        if line:
            allItems.append(line)

    infile.close()

    layer_size, layers = break_into_layers(argv.height, argv.width, allItems)

    if argv.phase == 1:

        sol = solutionPt1(layer_size, layers)
        print(f"image checksum: {sol}")
    elif argv.phase == 2:
        solutionPt2(layers, argv.height, argv.width)


def break_into_layers(height, width, items):
    layer_size = width * height
    layers = []
    for image in items:
        pos = 0
        while pos < len(image):
            layers.append(image[pos:(pos + layer_size)])
            pos += layer_size
    return layer_size, layers

def solutionPt1(layer_size, layers):

    lowest = layer_size + 1
    best_layer = None
    for layer in layers:
        zeroes = layer.count('0')
        if zeroes < lowest:
            lowest = zeroes
            best_layer = layer

    ones = best_layer.count('1')
    twoes = best_layer.count('2')

    return ones * twoes


def solutionPt2(layers, height, width):
    image = []
    raw_image = []
    for y in range(0, height):
        image.append([])
        for x in range(0, width):
            i = y * width + x
            ilayer = 0
            cur = '2'
            while cur == '2' and ilayer < len(layers):
                cur = layers[ilayer][i]
                ilayer += 1
            if cur == '0':
                # black - letting the console screen be the black
                image[y].append(' ')
            elif cur == '1':
                # white, using a unicode white box
                image[y].append(u"\u25A1")
                # image[y].append('1')
            else:
                # alpha, image had nothing on that pixel
                image[y].append(' ')
        raw_image.append(''.join(image[y]))

    output = '\n'.join(raw_image)
    print(output)



main(parser.parse_args())

