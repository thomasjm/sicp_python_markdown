#!/usr/bin/env python

import re
import sys

with open(sys.argv[1], "r") as input:
    content = input.read()

def unescape(inside):
    return inside.replace("\\\\", "\\").replace("\\^", "^").replace("\\_", "_")

regex = re.compile("\\\\\\\\\((.+?)\\\\\\\\\)")
while True:
    match = re.search(regex, content)
    if not match: break
    print("match: ", match.group(0))
    inside = match.group(1)
    inside = "$" + unescape(inside) + "$"
    print("inside: ", inside)
    content = content[0:match.start()] + inside + content[match.end():]

regex = re.compile("\\\\\\\\\\\\\[(.*)\\\\\\\\\\\\\]")
while True:
    match = re.search(regex, content)
    if not match: break
    inside = match.group(1)
    inside = "$$" + unescape(inside) + "$$"
    print("Match: ", match.group(0))
    print("Inside: ", inside)
    content = content[0:match.start()] + inside + content[match.end():]

with open(sys.argv[2], "w") as output:
    output.write(content)
