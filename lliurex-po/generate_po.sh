#!/bin/bash

FILE_POT="first-aid-kit/first-aid-kit.pot"
EXT="."
if [ ! -f $FILE_POT ]; then
	touch $FILE_POT
else
	rm $FILE_POT
	touch $FILE_POT
fi

for i; do 
    if [  ! -f $EXT$i ];then
	echo "Sorry NOT EXISTS: $EXT$i"
    else
	echo "Making pot for file: $EXT$i"
	xgettext --join-existing $EXT$i -o $FILE_POT
     fi
 done
 echo "Finished, you can review first-aid-kit/first-aid-kit.pot"