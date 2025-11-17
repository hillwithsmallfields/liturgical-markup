#!/usr/bin/env python3

"""Convert a simple liturgical markup to LaTeX."""

import argparse
import os
import re

import dobishem.storage as storage
import expressionive
from expressionive.expressionive import htmltags as T

class Visible:

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return f"<Visible {self.text}>"

    def add(self, text):
        self.text += text

class Heading(Visible):

    def __str__(self):
        return f"<Heading {self.text}>"

class Rubric(Visible):

    def __str__(self):
        return f"<Rubric {self.text}>"

class Verse(Visible):

    def __init__(self, text, continuation=None, number=None, divided=False):
        self.number = number
        self.text = text
        self.divided = divided
        self.continuation = continuation

    def __str__(self):
        return (f"<Verse {self.text} | {self.continuation}{' $' if self.divided else ''}>"
                if self.continuation
                else f"<Verse {self.text}{' $' if self.divided else ''}>")

    def add(self, text):
        if self.continuation is None:
            self.continuation = []
        self.continuation.append(text)

class OrderOfService:

    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def last(self):
        return self.items[-1]

    def add_to_last(self, text):
        self.last().add(text)

    def write_latex(self, outstream):
        """Write this service as LaTeX."""
        with open(out_file_name, 'w') as o:
            o.write("\usepackage{book-of-common-prayer}\n")

    def write_html(self, outstream):
        """Write this service as HTML."""
        pass

def ignore(service, line):
    pass

def blank(service, line):
    pass

def heading(service, line, text):
    service.add(Heading(text))

def rubric(service, line, text):
    service.add(Rubric(text))

def verse_initial(service, line, verse_number, text):
    service.add(Verse(text=text, number=verse_number))

def verse_initial_divided(service, line, verse_number, text):
    service.add(Verse(text=text, number=verse_number, divided=True))

def verse_continuation(service, line, text):
    service.add_to_last(text)

def verse_continuation_divided(service, line, text):
    service.add_to_last(text)

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

def litmu_parse_file(filename):
    service = OrderOfService()
    with open(filename) as instream:
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

def litmu_convert(source, output=None, verbose=False):
    service = litmu_parse_file(source)
    for item in service.items:
        print("  ", item)
    if output and output.endswith('.html'):
        service.write_html(output or os.path.splitext(source)[0] + ".html")
    else:
        service.write_latex(output or os.path.splitext(source)[0] + ".tex")

if __name__ == "__main__":
    litmu_convert(**get_args())
