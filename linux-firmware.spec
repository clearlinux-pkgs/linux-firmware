%define commit 936f3e98847e89f119b24e0fa50f7028d667c744

Name:           linux-firmware
Version:        20161215
Release:        20
License:        GPL-1.0+ GPL-2.0+ MIT Distributable
Summary:        Firmware files used by the Linux kernel
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://git.kernel.org/cgit/linux/kernel/git/firmware/linux-firmware.git/snapshot/linux-firmware-936f3e98847e89f119b24e0fa50f7028d667c744.tar.xz

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

%package extras
Summary:        Firmware files used by the Linux kernel
Group:          kernel

%description extras
Files from frirmware files

%package wifi
Summary:        Firmware files used by the Linux kernel
Group:          kernel

%description wifi
Files from frirmware files


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
rm -f %{buildroot}/usr/lib/firmware/inte-ucode/0f*

%files
%defattr(-,root,root,-)
/usr/lib/firmware/
%exclude /usr/lib/firmware/check_whence.py
%exclude /usr/lib/firmware/check_whence.pyc
%exclude /usr/lib/firmware/check_whence.pyo

%exclude /usr/lib/firmware/brcm
%exclude /usr/lib/firmware/amdgpu
%exclude /usr/lib/firmware/radeon
%exclude /usr/lib/firmware/nvidia

# wifi
%exclude /usr/lib/firmware/iwl*
%exclude /usr/lib/firmware/ath10k
%exclude /usr/lib/firmware/ath6k
%exclude /usr/lib/firmware/ar3k
%exclude /usr/lib/firmware/mrvl
%exclude /usr/lib/firmware/libertas
%exclude /usr/lib/firmware/ti-connectivity
%exclude /usr/lib/firmware/*wifi



%files extras
%defattr(-,root,root,-)
/usr/lib/firmware/amdgpu
/usr/lib/firmware/radeon
/usr/lib/firmware/nvidia

%files wifi
/usr/lib/firmware/iwl*
/usr/lib/firmware/brcm
/usr/lib/firmware/ath10k
/usr/lib/firmware/ath6k
/usr/lib/firmware/ar3k
/usr/lib/firmware/mrvl
/usr/lib/firmware/libertas
/usr/lib/firmware/ti-connectivity
/usr/lib/firmware/*wifi


%files doc
%defattr(-,root,root,-)
/usr/share/doc/linux-firmware


