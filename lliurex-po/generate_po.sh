#!/bin/bash
PYTHON_FILES="../first-aid-kit.install/usr/share/first-aid-kit/*.py"
UI_FILES="../first-aid-kit.install/usr/share/first-aid-kit/rsrc/first-aid-kit.ui"

#INDICATOR_FILE="../lliurex-remote-installer-indicator.install/usr/bin/lliurex-remote-installer-indicator"

FILE_POT="first-aid-kit/first-aid-kit.pot"

if [ ! -f $FILE_POT ]; then
	touch $FILE_POT
else
	rm $FILE_POT
	touch $FILE_POT
fi

for i in $UI_FILES ; do
	echo "Making pot for file: $i"
	xgettext --join-existing $i -o $FILE_POT
 done
 
 for i in $PYTHON_FILES ; do
	echo "Making pot for file: $i"
	xgettext --join-existing -L python $i -o $FILE_POT
 done
 
 echo "Finished, you can review first-aid-kit/first-aid-kit.pot"

#xgettext $UI_FILES $PYTHON_FILES -o lliurex-remote-installer-gui/lliurex-remote-installer-gui.pot
#xgettext --join-existing -L python $INDICATOR_FILE -o lliurex-remote-installer-gui/lliurex-remote-installer-gui.pot