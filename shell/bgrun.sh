#!/bin/bash

if [ $# -eq 0 ]; then
	echo "Usage: bgrun <program> [arguments]"
	exit 1
fi

"$@" > /dev/null 2>&1 &

exit 0

