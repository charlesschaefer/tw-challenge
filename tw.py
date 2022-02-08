#!/usr/bin/python

import sys, getopt, os

from src import FileParser, DiceRoller, OutputFormatter

def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'hi:o:p')
    except getopt.GetoptError:
        help()
    
    input_file = ''
    output_file = ''
    pretty = False

    for opt, arg in opts:
        if opt == '-i':
            input_file = arg
        elif opt == '-o':
            output_file = arg
        elif opt == '-p':
            pretty = True
    
    if input_file == '':
        help()
    
    if not os.path.isfile(input_file):
        print("The provided input_file doesn't exist")
        print("======================================")
        help()
    
    parse(input_file, output_file, pretty)


def parse(input_file, output_file, pretty):
    with open(input_file) as input:
        lines = input.read()
    
    parser = FileParser(lines)
    parsed_file = parser.parse_file()

    roller = DiceRoller(parsed_file)
    rolled = roller.roll_all()

    formatter = OutputFormatter(rolled)
    json = formatter.format(not pretty)

    if output_file != '':
        with open(output_file, 'w') as output:
            output.write(json)
    else:
        print(json)




def help():
    help = """
    python tw.py -i <input_file> [-o <output_file>] [-p]
        -i <input_file>: a path to the input file, with the dice lines
        -o <output_file>: (optional) the output file to where the json must be writen
        -p: (optional) if the content must be formatted as a single-line json or a preety one
    """
    print(help)
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])