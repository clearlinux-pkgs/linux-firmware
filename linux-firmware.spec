Name:           linux-firmware
Version:        20250311
Release:        238
License:        GPL-1.0+ GPL-2.0+ MIT Distributable
Summary:        Firmware files used by the Linux kernel
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/snapshot/linux-firmware-20250311.tar.gz
Source10:       https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/archive/microcode-20250211.tar.gz
Source11:       https://github.com/intel/sound-open-firmware-binaries/archive/v1.1-apl.tar.gz
Requires:       linux-firmware-doc
BuildRequires:	rdfind

Patch0001:	0001-Compress-firmware-with-ZST-by-default.patch
Patch0002:	zstd-rsyncable.patch

# Force brp-strip* to be no-ops... beginning with rpm 4.17, the scripts try to
# strip non-executable ELF content, which fails the build when attempting to
# process *.nffw files (ELF content with unknown arch). But we should not be
# stripping firmware files at all...
%define __strip /bin/true

%description
This package includes firmware files required for some devices to
operate.

%package doc
Summary:        Firmware Licences files used by the Linux kernel
Group:          kernel

%description doc
Licence files from firmware files

%package extras
Summary:        Firmware files used by the Linux kernel
Group:          kernel

%description extras
Files from firmware files

%package wifi
Summary:        Firmware files used by the Linux kernel
Group:          kernel
Requires:       linux-firmware
Requires:       wireless-regdb-master

%description wifi
Files from firmware files

%package i915-cpio
Summary:        cpio file with i915 firmware files
Group:          kernel

%description i915-cpio
CPIO file from i915 firmware files

%package qat-cpio
Summary:        cpio file with Intel QuickAssist firmware files
Group:          kernel

%description qat-cpio
CPIO file from qat_* firmware files

%package ucode-cpio
Summary:        cpio file with Intel and AMD microcode
Group:          kernel

%description ucode-cpio
CPIO file containing Intel and AMD microcode files, needed for early load

%prep
%setup -q -n linux-firmware-20250311

%patch -P 0001 -p1
%patch -P 0002 -p1

%install
mkdir -p %{buildroot}/usr/share/doc/linux-firmware
cp WHENCE LICENS* GPL* %{buildroot}/usr/share/doc/linux-firmware
%make_install FIRMWAREDIR=/usr/lib/firmware
make DESTDIR=%{buildroot}/usr dedup
tar -axf %{SOURCE10}
cp -a Intel-Linux-Processor-Microcode-Data-Files-microcode-*/intel-ucode %{buildroot}/usr/lib/firmware

# All our kernels have the required kernel update for the microcode with caveats
#
cp  Intel-Linux-Processor-Microcode-Data-Files-microcode-*/intel-ucode-with-caveats/06*  %{buildroot}/usr/lib/firmware/intel-ucode/

rm -f %{buildroot}/usr/lib/firmware/intel-ucode/0f*
tar -axf %{SOURCE11}
cp -a sound-open-firmware-binaries-1.1-apl/* %{buildroot}/usr/lib/firmware/intel

# Remove unmaintained firmware
rm -f %{buildroot}/usr/lib/firmware/phanfw.bin
rm -f %{buildroot}/usr/lib/firmware/mediatek/mt8195/scp.img

# Create the i915 CPIO file
mkdir -p %{buildroot}/usr/lib/initrd.d
mkdir -p cpio/usr/lib/firmware/i915
ln    -s usr/lib  cpio/lib
# copy the i915 DMC binaries, use -9e for maximum compression, systems
# nowdays have more than enough memory to compress and decompress with -9e
cp -a %{buildroot}/usr/lib/firmware/i915/*  cpio/usr/lib/firmware/i915
(
  cd cpio
  find . -type f -name '*.zst' -exec unzstd --rm {} \;
  find . -type l -name '*.zst' | while read link; do target=$(readlink "${link}"); ln -s "${target%.zst}" "${link%.zst}"; rm "${link}"; done
  find . | cpio --create --format=newc > %{buildroot}/usr/lib/initrd.d/i915-firmware.cpio
  zstd --rm %{buildroot}/usr/lib/initrd.d/i915-firmware.cpio
)

mkdir -p intel-qat-cpio/usr/lib/firmware/
cp -a %{buildroot}/usr/lib/firmware/qat_*  intel-qat-cpio/usr/lib/firmware/
(
  cd intel-qat-cpio
  find . | cpio --create --format=newc  > %{buildroot}/usr/lib/initrd.d/qat-firmware.cpio
)
# Create the early-ucode CPIO file (cannot be compressed)
# See: https://www.kernel.org/doc/html/latest/x86/microcode.html
mkdir -p early-ucode-cpio/kernel/x86/microcode
cat %{buildroot}/usr/lib/firmware/intel-ucode/* > early-ucode-cpio/kernel/x86/microcode/GenuineIntel.bin
cat %{buildroot}/usr/lib/firmware/amd-ucode/*.bin > early-ucode-cpio/kernel/x86/microcode/AuthenticAMD.bin
(
  cd early-ucode-cpio
  find . | cpio --create --format=newc --owner=0:0 > %{buildroot}/usr/lib/initrd.d/00-early-ucode.cpio
)

%files
%defattr(-,root,root,-)
/usr/lib/firmware/
%exclude /usr/lib/firmware/liquidio/lio_23xx_vsw.bin*
%exclude /usr/lib/firmware/check_whence.py*

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

# these are in alsa-firmware instead
%exclude /usr/lib/firmware/aica_firmware.bin*
%exclude /usr/lib/firmware/asihpi/dsp5000.bin*
%exclude /usr/lib/firmware/asihpi/dsp6200.bin*
%exclude /usr/lib/firmware/asihpi/dsp6205.bin*
%exclude /usr/lib/firmware/asihpi/dsp6400.bin*
%exclude /usr/lib/firmware/asihpi/dsp6600.bin*
%exclude /usr/lib/firmware/asihpi/dsp8700.bin*
%exclude /usr/lib/firmware/asihpi/dsp8900.bin*
%exclude /usr/lib/firmware/cs46xx/*
%exclude /usr/lib/firmware/ctefx-desktop.bin*
%exclude /usr/lib/firmware/ctefx-r3di.bin*
%exclude /usr/lib/firmware/ctefx.bin*
%exclude /usr/lib/firmware/ctspeq.bin*
%exclude /usr/lib/firmware/digiface_firmware.bin*
%exclude /usr/lib/firmware/digiface_firmware_rev11.bin*
%exclude /usr/lib/firmware/ea/*
%exclude /usr/lib/firmware/emu/*
%exclude /usr/lib/firmware/ess/*
%exclude /usr/lib/firmware/korg/k1212.dsp*
%exclude /usr/lib/firmware/mixart/*
%exclude /usr/lib/firmware/multiface_firmware.bin*
%exclude /usr/lib/firmware/multiface_firmware_rev11.bin*
%exclude /usr/lib/firmware/pcxhr/*
%exclude /usr/lib/firmware/rpm_firmware.bin*
%exclude /usr/lib/firmware/sb16/*
%exclude /usr/lib/firmware/turtlebeach/*
%exclude /usr/lib/firmware/vx/*
%exclude /usr/lib/firmware/yamaha/*

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
/usr/lib/firmware/mwlwifi
/usr/lib/firmware/rtlwifi
/usr/lib/firmware/ti-connectivity

%files doc
%defattr(-,root,root,-)
/usr/share/doc/linux-firmware

%files i915-cpio
%defattr(-,root,root,-)
/usr/lib/initrd.d/i915-firmware.cpio.zst

%files qat-cpio
%defattr(-,root,root,-)
/usr/lib/initrd.d/qat-firmware.cpio

%files ucode-cpio
%defattr(-,root,root,-)
/usr/lib/initrd.d/00-early-ucode.cpio
