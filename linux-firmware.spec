%define commit a4bbc8112cc04fcc0e0861e8b72197b6cb83ab83

Name:           linux-firmware
Version:        20150619
Release:        7
License:        GPL-1.0+ GPL-2.0+ MIT Distributable
Summary:        Firmware files used by the Linux kernel
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://git.kernel.org/cgit/linux/kernel/git/firmware/linux-firmware.git/snapshot/linux-firmware-a4bbc8112cc04fcc0e0861e8b72197b6cb83ab83.tar.xz
Patch0:         0001-Allow-FIRMWAREDIR-to-be-overriden.patch

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
%make_install FIRMWAREDIR=/usr/lib/firmware

# Keep in sync with the doc macro
find %{buildroot} -name "LICENS*" -or -name "GPL*" -or -name "WHENCE" -exec /bin/rm {} \;

%files
%defattr(-,root,root,-)
/usr/lib/firmware/


%files doc
%defattr(-,root,root,-)
%doc WHENCE LICENS* GPL*

