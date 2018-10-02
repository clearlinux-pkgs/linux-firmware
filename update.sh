#!/bin/bash

unset no_proxy
VERSION=`curl -s -L  https://git.kernel.org/cgit/linux/kernel/git/firmware/linux-firmware.git/commit/ | grep parent | cut -f6 -d">" | cut -f1 -d"<"`
OLDVERSION=`cat linux-firmware.spec | head -1 | cut -f3 -d" "`

if [ "$VERSION" == "$OLDVERSION" ] ; then
	echo "Nothing changed $OLDVERSION == $VERSION"
	exit 0
fi
	

echo "Updating from $OLDVERSION to $VERSION"

sed -i -e "s/$OLDVERSION/$VERSION/g" linux-firmware.spec
make generateupstream
git commit -a -m "Update to upstream commit $VERSION"
make bump
make koji
