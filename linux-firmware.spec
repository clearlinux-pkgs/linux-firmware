%define commit c555311c5ad0ad26d60db92f4f730c3c60fad727

Name:           linux-firmware
Version:        20161215
Release:        12
License:        GPL-1.0+ GPL-2.0+ MIT Distributable
Summary:        Firmware files used by the Linux kernel
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://git.kernel.org/cgit/linux/kernel/git/firmware/linux-firmware.git/snapshot/linux-firmware-c555311c5ad0ad26d60db92f4f730c3c60fad727.tar.xz

Source10:	intel-microcode2ucode.c
Source11:	microcode.dat
Patch0:         0001-Allow-FIRMWAREDIR-to-be-overriden.patch
Requires:       linux-firmware-doc

%description
This package includes firmware files required for some devices to
operate.

%package doc
Summary:        Firmware Licences files used by the Linux kernel
Group:          kernel

%description doc
Licence files from frirmware files


%prep
%setup -q -n linux-firmware-%{commit}
%patch0 -p1


%install
mkdir -p %{buildroot}/usr/share/doc/linux-firmware
cp WHENCE LICENS* GPL* %{buildroot}/usr/share/doc/linux-firmware
%make_install FIRMWAREDIR=/usr/lib/firmware
gcc %{SOURCE10} -o m2u
./m2u %{SOURCE11}
chmod -R a+rx intel-ucode
cp -a intel-ucode %{buildroot}/usr/lib/firmware

%files
%defattr(-,root,root,-)
/usr/lib/firmware/
%exclude /usr/lib/firmware/check_whence.py
%exclude /usr/lib/firmware/check_whence.pyc
%exclude /usr/lib/firmware/check_whence.pyo


%files doc
%defattr(-,root,root,-)
/usr/share/doc/linux-firmware

