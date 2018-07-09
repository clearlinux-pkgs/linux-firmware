%define commit fe4a9d49d44c40a7bc32cdd9529e6a5c8ac92519

Name:           linux-firmware
Version:        20180000
Release:        56
License:        GPL-1.0+ GPL-2.0+ MIT Distributable
Summary:        Firmware files used by the Linux kernel
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/snapshot/linux-firmware-fe4a9d49d44c40a7bc32cdd9529e6a5c8ac92519.tar.gz
Source10:       https://downloadmirror.intel.com/27776/eng/microcode-20180425.tgz
Source11:       https://github.com/intel/sound-open-firmware-binaries/archive/v1.1-apl.tar.gz
Source12:       http://localhost/cgit/projects/ipu4fw/snapshot/ipu4fw-1.0.0-2084.127908d.tar.bz2
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
Requires:	wireless-regdb-master
%description wifi
Files from frirmware files

%package ipu4
Summary:        IPU4 Firmware files used by the Linux kernel
Group:          kernel

%description ipu4
Files from ipu4 frirmware


%prep
%setup -q -n linux-firmware-%{commit}


%install
mkdir -p %{buildroot}/usr/share/doc/linux-firmware
cp WHENCE LICENS* GPL* %{buildroot}/usr/share/doc/linux-firmware
%make_install FIRMWAREDIR=/usr/lib/firmware
tar -axf %{SOURCE10}
cp -a intel-ucode %{buildroot}/usr/lib/firmware


# All our kernels have the required kernel update for the microcode with caveats
#
cp  intel-ucode-with-caveats/06*  %{buildroot}/usr/lib/firmware/intel-ucode/


rm -f %{buildroot}/usr/lib/firmware/intel-ucode/0f*
tar -axf %{SOURCE11}
cp -a sound-open-firmware-binaries-1.1-apl/* %{buildroot}/usr/lib/firmware/intel
tar -axf %{SOURCE12}

# Install IPU4
cp -a ipu4fw-1.0.0-2084.127908d/lib/firmware/ipu4_cpd_b0.bin %{buildroot}/usr/lib/firmware/ipu4_cpd_b0.bin
mkdir -p %{buildroot}/usr/lib/modprobe.d
mkdir -p %{buildroot}/usr/lib/modules-load.d
cp  ipu4fw-1.0.0-2084.127908d/etc/modprobe.d/ipu_ops.conf %{buildroot}/usr/lib/modprobe.d/ipu_ops.conf
cp  ipu4fw-1.0.0-2084.127908d/etc/modules-load.d/ipu.conf %{buildroot}/usr/lib/modules-load.d/ipu.conf


%files
%defattr(-,root,root,-)
/usr/lib/firmware/
%exclude /usr/lib/firmware/liquidio/lio_23xx_vsw.bin
%exclude /usr/lib/firmware/check_whence.py
%exclude /usr/lib/firmware/check_whence.pyc
%exclude /usr/lib/firmware/check_whence.pyo

# gpu
%exclude /usr/lib/firmware/amdgpu
%exclude /usr/lib/firmware/radeon
%exclude /usr/lib/firmware/nvidia

# wifi
%exclude /usr/lib/firmware/iwl*
%exclude /usr/lib/firmware/brcm
%exclude /usr/lib/firmware/ath10k
%exclude /usr/lib/firmware/ath6k
%exclude /usr/lib/firmware/ar3k
%exclude /usr/lib/firmware/mrvl
%exclude /usr/lib/firmware/libertas
%exclude /usr/lib/firmware/ti-connectivity
%exclude /usr/lib/firmware/*wifi

# IPU4
%exclude /usr/lib/firmware/ipu4_cpd_b0.bin
%exclude /usr/lib/modprobe.d/ipu_ops.conf
%exclude /usr/lib/modules-load.d/ipu.conf

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

%files ipu4
/usr/lib/firmware/ipu4_cpd_b0.bin
/usr/lib/modprobe.d/ipu_ops.conf
/usr/lib/modules-load.d/ipu.conf

%files doc
%defattr(-,root,root,-)
/usr/share/doc/linux-firmware


