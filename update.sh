#!/bin/bash
set -e -o pipefail

unset no_proxy
LINUXFW=0
UCODE=0
VERSION=`git ls-remote -q --refs https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git |tail -n 1 |cut -d '/' -f3`
OLDVERSION=`grep ^Version linux-firmware.spec | cut -d: -f2 | sed 's/ //g'`

UCVERSION=`git ls-remote -q --refs https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files | tail -n 1 | sed 's/.*microcode-\([0-9]*\)/\1/'`
UCOLDVERSION=`grep ^Source10 linux-firmware.spec | sed 's/.*microcode-\([0-9a-f]*\)\.tar\.gz/\1/'`

echo "--linux-firmware: $VERSION--"
if [ "$VERSION" == "$OLDVERSION" ] ; then
	echo "Nothing changed linux-firmware $OLDVERSION == $VERSION"
	LINUXFW=1
fi

echo "--microcode: $UCVERSION--"
if [ "$UCVERSION" == "$UCOLDVERSION" ] ; then
	echo "Nothing changed microcode $UCOLDVERSION == $UCVERSION"
	UCODE=1
fi

if [ "$LINUXFW" -eq 1 ] && [ "$UCODE" -eq 1 ]; then
    exit 0
fi

MSG="Update to"
if [ "$LINUXFW" -eq 0 ]; then
    echo "Updating linux-firmware from $OLDVERSION to $VERSION"

    sed_cmd="/^Version.*:/s/$OLDVERSION/$VERSION/g"
    echo sed -i -e "$sed_cmd" linux-firmware.spec
    sed -i -e "$sed_cmd" linux-firmware.spec

    sed_cmd="s/linux-firmware-$OLDVERSION/linux-firmware-$VERSION/g"
    echo sed -i -e "$sed_cmd" linux-firmware.spec
    sed -i -e "$sed_cmd" linux-firmware.spec

    MSG="$MSG linux-firmware $VERSION"
fi
if [ "$UCODE" -eq 0 ]; then
    echo "Updating microcode from $UCOLDVERSION to $UCVERSION"

    sed_cmd="s/microcode-$UCOLDVERSION/microcode-$UCVERSION/g"
    echo sed -i -e "$sed_cmd" linux-firmware.spec
    sed -i -e "$sed_cmd" linux-firmware.spec
    MSG="$MSG microcode $UCVERSION"
fi

make generateupstream || { 2>&1 echo "Some upstream URLs cannot be fetched."; exit 1; }
#git diff
#echo -n "Press ENTER to commit, ^C to abort..."
#read BAILOUT

make bumpnogit
git commit -a -m "$MSG"

export no_proxy="intel.com"
make koji-nowait
