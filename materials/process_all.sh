#!/bin/bash

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

mkdir -p rendered

$SCRIPTDIR/process.sh Chapter1.html ..
$SCRIPTDIR/process.sh Chapter2.html ..
$SCRIPTDIR/process.sh Chapter3.html ..
$SCRIPTDIR/process.sh Chapter4.html ..
$SCRIPTDIR/process.sh Chapter5.html ..
