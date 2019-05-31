%define commit 1f8ebdfc2634944cc70c1ca3b4f167e39a7109c1

Name:           linux-firmware
Version:        20180000
Release:        113
License:        GPL-1.0+ GPL-2.0+ MIT Distributable
Summary:        Firmware files used by the Linux kernel
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/snapshot/linux-firmware-1f8ebdfc2634944cc70c1ca3b4f167e39a7109c1.tar.gz
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

# Remove unmaintained firmware
rm -f %{buildroot}/usr/lib/firmware/phanfw.bin

# Create the i915 CPIO file
mkdir -p %{buildroot}/usr/lib/initrd.d
ln -s  usr/lib %{buildroot}/lib
mkdir -p cpio/usr/lib/firmware/i915
mkdir -p cpio/usr/lib/firmware/intel-ucode
# copy intel-ucode and dmc
cp -a %{buildroot}/usr/lib/firmware/i915/*_dmc_*  cpio/usr/lib/firmware/i915
cp -a %{buildroot}/usr/lib/firmware/intel-ucode/* cpio/usr/lib/firmware/intel-ucode
# copy ucode
(
  cd cpio
  find . | cpio --create --format=newc \
    | xz --check=crc32 --lzma2=dict=512KiB > %{buildroot}/usr/lib/initrd.d/i915-firmware.cpio.xz
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
