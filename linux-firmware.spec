%define commit bfeee58b50208808969bb18b7f297683ba581dc1

Name:           linux-firmware
Version:        20151106
Release:        2
License:        GPL-1.0+ GPL-2.0+ MIT Distributable
Summary:        Firmware files used by the Linux kernel
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://git.kernel.org/cgit/linux/kernel/git/firmware/linux-firmware.git/snapshot/linux-firmware-bfeee58b50208808969bb18b7f297683ba581dc1.tar.xz

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


%build

#Copy to .save the wanted firmware files 
mkdir .save
cp ath9k_htc/* .save
cp WHENCE LICENCE.atheros_firmware .save
rm -rf *

%install

# Create firmware directory 
mkdir -p %{buildroot}/usr/lib/firmware

# Copy saved files to firmware directory
cp .save/* %{buildroot}/usr/lib/firmware

# Create link names to firmwares files
ln -s htc_7010-1.4.0.fw %{buildroot}/usr/lib/firmware/htc_7010.fw
ln -s htc_9271-1.4.0.fw %{buildroot}/usr/lib/firmware/htc_9271.fw

%files
%defattr(-,root,root,-)
/usr/lib/firmware/htc_7010*
/usr/lib/firmware/htc_9271*

%files doc
%defattr(-,root,root,-)
/usr/lib/firmware/WHENCE
/usr/lib/firmware/LICEN*
