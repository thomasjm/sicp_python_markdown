#!/usr/bin/env python

import re
import sys

with open(sys.argv[1], "r") as input:
    lines = input.readlines()

newLines = []

def tryReadIndentedBlock(codeLines, i, linesToReturn):
    if codeLines[i].startswith(">>> "):
        while i < len(codeLines) and (codeLines[i].startswith(">>> ") or codeLines[i].startswith("    ") or codeLines[i].strip() == ""):
            if codeLines[i].strip() == "":
                linesToReturn.append("\n")
            else:
                linesToReturn.append(codeLines[i][4:])
            i += 1

    return i

def makeOutput(text):
    return '<html><div class="codeparent python"><pre class="stdout"><code>%s</code></pre></div></html>\n' % text

def tryReadOutput(codeLines, i, linesToReturn):
    stdout = []
    gotSomething = False

    while i < len(codeLines) and not (codeLines[i].startswith(">>> ")):
        gotSomething = True
        stdout.append(codeLines[i])
        i += 1

    if gotSomething:
        if len(stdout) == 1:
            text = stdout[0].strip()
        else:
            text = "".join(stdout)

        linesToReturn.append("```" + "\n" + makeOutput(text))

    return i

def transformCodeLines(codeLines, startLine, endLine):
    linesToReturn = [startLine]

    i = 0
    while i < len(codeLines):
        i = tryReadIndentedBlock(codeLines, i, linesToReturn)

        if i < len(codeLines):
            j = tryReadOutput(codeLines, i, linesToReturn)
            if j > i:
                # We read some output

                if j < len(codeLines):
                    # More stuff is to come
                    linesToReturn.append("\n" + startLine)

                i = j
            else:
                # No output was read
                # If there's still code to read after this, start a new block and continue
                if i < len(codeLines):
                    linesToReturn.append("\n" + "```" + "\n\n" + startLine)
                else:
                    linesToReturn.append("```\n")
        else:
            linesToReturn.append("```\n")

    return linesToReturn

i = 0
while i < len(lines):
    line = lines[i];

    if line.startswith("``` {") and "python" in line:
        codeLines = []
        j = i + 1
        while not lines[j].startswith("```"):
            codeLines.append(lines[j])
            j += 1

        # Hop over the final close delimiter, the code line transformation will deal with it
        j += 1

        codeLines = transformCodeLines(codeLines, line, "```")
        newLines.extend(codeLines)

        i = j
    else:
        newLines.append(lines[i])
        i += 1


with open(sys.argv[2], "w") as output:
    for line in newLines:
        output.write(line)
