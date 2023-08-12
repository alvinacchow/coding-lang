# project3.py
#
# ICS 33 Winter 2023
# Project 3: Why Not Smile?
#
# The main module that executes your Grin interpreter.
#
# WHAT YOU NEED TO DO: You'll need to implement the outermost shell of your
# program here, but consider how you can keep this part as simple as possible,
# offloading as much of the complexity as you can into additional modules in
# the 'grin' package, isolated in a way that allows you to unit test them.

import grin

def read_input() -> list:
    """Reads and returns a list of the input from the standard input"""
    lines = []
    while True:
        line = input()
        if line.strip() != '.':
            lines.append(line)
        else:
            return lines

def main() -> None:
    """Runs the main program by reading and processing the grin input"""
    lines = read_input()
    program = grin.State(lines)
    program.process_grin()

if __name__ == '__main__':
    main()
