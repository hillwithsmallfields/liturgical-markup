#!/usr/bin/env python3

"""Convert a simple liturgical markup to LaTeX."""

import argparse
import os
import re

def ignore(line):
    pass

def blank(line):
    pass

def heading(line, text):
    print("heading", text)

def rubric(line, text):
    pass

def verse_initial(line, verse_number, text):
    print("verse_initial number", verse_number, "has text", text)

def verse_initial_divided(line, verse_number, text):
    print("verse_initial number", verse_number, "has text", text, "and divider")

def verse_continuation(line, text):
    print("verse_continuation text", text)

def verse_continuation_divided(line, text):
    print("verse_continuation text", text, "and divider")

LINE_HANDLERS = [
    (r" *$", blank),
    (r"#.+", ignore),
    (r"% *(.+)", heading),
    (r"! *(.+)", rubric),
    (r" *([0-9]+) +(.+) *[$♦]", verse_initial_divided),
    (r" *([0-9]+) +(.+)", verse_initial),
    (r" +(.+) *[$♦]", verse_continuation_divided),
    (r" +(.+)", verse_continuation),
]

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", "-o")
    parser.add_argument("source")
    parser.add_argument("--verbose", "-v", action='store_true')
    return vars(parser.parse_args())

def litmu2latex_main(source, output=None, verbose=False):
    with open(source) as instream, open(output or os.path.splitext(source)[0] + ".tex", 'w') as outstream:
        for line in instream:
            line = line.rstrip()
            done = False
            for pattern, action in LINE_HANDLERS:
                if (m := re.match(pattern, line)):
                    action(line, *m.groups())
                    done = True
                    break
            if not done:
                print('Could not do anything with "%s"' % line)

if __name__ == "__main__":
    litmu2latex_main(**get_args())
