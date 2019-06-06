#!/bin/bash

unset no_proxy
VERSION=`git ls-remote -q --refs https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git |tail -n 1 |cut -d '/' -f3`
OLDVERSION=`grep ^Version linux-firmware.spec | cut -d: -f2 | sed 's/ //g'`

echo "--$VERSION--"
if [ "$VERSION" == "$OLDVERSION" ] ; then
	echo "Nothing changed $OLDVERSION == $VERSION"
	exit 0
fi
	

echo "Updating from $OLDVERSION to $VERSION"

echo sed -i -e "s/$OLDVERSION/$VERSION/g" linux-firmware.spec
sed -i -e "s/$OLDVERSION/$VERSION/g" linux-firmware.spec
make generateupstream || { 2>&1 echo "Some upstream URLs cannot be fetched."; exit 1; }
git diff
echo -n "Press ENTER to commit, ^C to abort..."
read BAILOUT
git commit -a -m "Update to upstream tag $VERSION"
make bump
make koji
