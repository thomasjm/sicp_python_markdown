#!/bin/bash

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
FILE=$1
OUT=$SCRIPTDIR/$2

pandoc $FILE --wrap=none --from=html-raw_html --to=markdown-raw_html-header_attributes-link_attributes --atx-headers  -o $OUT

# Make sure block quotes have a space for empty lines
sed -i 's/^>$/> /g' $OUT

# Remove special classes on backticks and links
sed -i 's/{\.docutils \.literal}//g' $OUT
sed -i 's/{\.reference \.external}//g' $OUT

# Set the code block headers reasonably
sed -i 's/{\.doctest-block}/{\.python}/g' $OUT

sed -i 's/{\.literal-block}/{}/g' $OUT
