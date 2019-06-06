Name:           linux-firmware
Version:        20190514
Release:        117
License:        GPL-1.0+ GPL-2.0+ MIT Distributable
Summary:        Firmware files used by the Linux kernel
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/snapshot/linux-firmware-20190514.tar.gz
Source10:       https://downloadmirror.intel.com/28039/eng/microcode-20180807.tgz
Source11:       https://github.com/intel/sound-open-firmware-binaries/archive/v1.1-apl.tar.gz
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

%package i915-cpio
Summary:        cpio file with i915 firmware files
Group:          kernel

%description i915-cpio
CPIO file from i915 frirmware files

%package ucode-cpio
Summary:        cpio file with intel-ucode file
Group:          kernel

%description ucode-cpio
CPIO file containing Intel microcode file, needed for early load

%prep
%setup -q -n linux-firmware-%{version}


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

# Remove unmaintained firmware
rm -f %{buildroot}/usr/lib/firmware/phanfw.bin

# Create the i915 CPIO file
mkdir -p %{buildroot}/usr/lib/initrd.d
mkdir -p cpio/usr/lib/firmware/i915
ln    -s usr/lib  cpio/lib
# copy the i915 DMC binaries
cp -a %{buildroot}/usr/lib/firmware/i915/*_dmc_*  cpio/usr/lib/firmware/i915
(
  cd cpio
  find . | cpio --create --format=newc \
    | xz --check=crc32 --lzma2=dict=512KiB > %{buildroot}/usr/lib/initrd.d/i915-firmware.cpio.xz
)

# Create the intel-ucode CPIO file (cannot be compressed)
# See: https://www.kernel.org/doc/html/latest/x86/microcode.html
mkdir -p intel-ucode-cpio/kernel/x86/microcode
cat %{buildroot}/usr/lib/firmware/intel-ucode/* > intel-ucode-cpio/kernel/x86/microcode/GenuineIntel.bin
(
  cd intel-ucode-cpio
  find . | cpio --create --format=newc --owner=0:0 > %{buildroot}/usr/lib/initrd.d/00-intel-ucode.cpio
)

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

%files i915-cpio
%defattr(-,root,root,-)
/usr/lib/initrd.d/i915-firmware.cpio.xz

%files ucode-cpio
%defattr(-,root,root,-)
/usr/lib/initrd.d/00-intel-ucode.cpio
