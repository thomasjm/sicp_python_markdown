#!/bin/bash

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
FILE=$1
OUT=$SCRIPTDIR/$2

pandoc $FILE --wrap=none --from=html-raw_html --to=markdown-raw_html-header_attributes  -o $OUT

