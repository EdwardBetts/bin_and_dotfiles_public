#!/bin/bash
FILE=size.txt

generate_size_file()
{
	TMP=$(mktemp)
	ls -lS --block-size=1 | awk ' {print $5,$6,$7,$8}' >$TMP
	du -s --block-size=1 */ >>$TMP
	sort -n $TMP >$FILE
}

if [ -s $FILE ]
then
	echo "$FILE exists. Overwrite?(y/n)"
	read ans
	case $ans in
	  y|Y|yes) generate_size_file ;;
	  *) echo "Using existing file." ;;
	esac
else
	generate_size_file
fi

cat $FILE

