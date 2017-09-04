#!/bin/bash

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

mkdir -p rendered

$SCRIPTDIR/process.sh Chapter1.html rendered/Chapter1.md
$SCRIPTDIR/process.sh Chapter2.html rendered/Chapter2.md
$SCRIPTDIR/process.sh Chapter3.html rendered/Chapter3.md
$SCRIPTDIR/process.sh Chapter4.html rendered/Chapter4.md
$SCRIPTDIR/process.sh Chapter5.html rendered/Chapter5.md
