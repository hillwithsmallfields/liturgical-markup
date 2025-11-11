#!/usr/bin/env python3

"""Convert a simple liturgical markup to LaTeX."""

import argparse
import os
import re

class Visible:

    def __init__(self, text):
        self.text = text

    def add(self, text):
        self.text += text

class Heading(Visible):
    pass

class Rubric(Visible):
    pass

class Verse(Visible):

    def __init__(self, first, second=None, number=None):
        self.number = number
        self.text = first
        self.second = second

class OrderOfService:

    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def last(self):
        return self.items[-1]

    def add_to_last(self, text):
        self.last().add(text)

def ignore(service, line):
    pass

def blank(service, line):
    pass

def heading(service, line, text):
    print("heading", text)
    service.add(Heading(text))

def rubric(service, line, text):
    service.add(Rubric(text))

def verse_initial(service, line, verse_number, text):
    print("verse_initial number", verse_number, "has text", text)
    service.add(first=text, number=number)

def verse_initial_divided(service, line, verse_number, text):
    print("verse_initial number", verse_number, "has text", text, "and divider")

def verse_continuation(service, line, text):
    print("verse_continuation text", text)

def verse_continuation_divided(service, line, text):
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
    service = OrderOfService()
    with open(source) as instream, open(output or os.path.splitext(source)[0] + ".tex", 'w') as outstream:
        for line in instream:
            line = line.rstrip()
            done = False
            for pattern, action in LINE_HANDLERS:
                if (m := re.match(pattern, line)):
                    action(service, line, *m.groups())
                    done = True
                    break
            if not done:
                print('Could not do anything with "%s"' % line)

if __name__ == "__main__":
    litmu2latex_main(**get_args())
