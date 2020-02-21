Name:           linux-firmware
Version:        20200122
Release:        133
License:        GPL-1.0+ GPL-2.0+ MIT Distributable
Summary:        Firmware files used by the Linux kernel
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/snapshot/linux-firmware-20200122.tar.gz
Source10:       https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/archive/microcode-20191115.tar.gz
Source20:       https://github.com/intel/sound-open-firmware-binaries/archive/v1.1-apl.tar.gz
Source30:       https://github.com/thesofproject/sof/releases/download/v1.4.2/sof-apl-v1.4.2.ldc
Source31:       https://github.com/thesofproject/sof/releases/download/v1.4.2/sof-apl-v1.4.2.ri
Source32:       https://github.com/thesofproject/sof/releases/download/v1.4.2/sof-bdw.ldc
Source33:       https://github.com/thesofproject/sof/releases/download/v1.4.2/sof-bdw.ri
Source34:       https://github.com/thesofproject/sof/releases/download/v1.4.2/sof-byt.ldc
Source35:       https://github.com/thesofproject/sof/releases/download/v1.4.2/sof-byt.ri
Source36:       https://github.com/thesofproject/sof/releases/download/v1.4.2/sof-cht.ldc
Source37:       https://github.com/thesofproject/sof/releases/download/v1.4.2/sof-cht.ri
Source38:       https://github.com/thesofproject/sof/releases/download/v1.4.2/sof-cnl-v1.4.2.ldc
Source39:       https://github.com/thesofproject/sof/releases/download/v1.4.2/sof-cnl-v1.4.2.ri
Source40:       https://github.com/thesofproject/sof/releases/download/v1.4.2/sof-icl-v1.4.2.ldc
Source41:       https://github.com/thesofproject/sof/releases/download/v1.4.2/sof-icl-v1.4.2.ri
Source42:       https://github.com/thesofproject/sof/releases/download/v1.4.2/sof-imx8.ldc
Source43:       https://github.com/thesofproject/sof/releases/download/v1.4.2/sof-imx8.ri

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
Files from firmware files

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
CPIO file from i915 firmware files

%package qat-cpio
Summary:        cpio file with Intel QuickAssist firmware files
Group:          kernel

%description qat-cpio
CPIO file from qat_* firmware files

%package ucode-cpio
Summary:        cpio file with intel-ucode file
Group:          kernel

%description ucode-cpio
CPIO file containing Intel microcode file, needed for early load

%prep
%setup -q -n linux-firmware-20200122


%install
mkdir -p %{buildroot}/usr/share/doc/linux-firmware
cp WHENCE LICENS* GPL* %{buildroot}/usr/share/doc/linux-firmware
%make_install FIRMWAREDIR=/usr/lib/firmware
tar -axf %{SOURCE10}
cp -a Intel-Linux-Processor-Microcode-Data-Files-microcode-*/intel-ucode %{buildroot}/usr/lib/firmware

# All our kernels have the required kernel update for the microcode with caveats
#
cp  Intel-Linux-Processor-Microcode-Data-Files-microcode-*/intel-ucode-with-caveats/06*  %{buildroot}/usr/lib/firmware/intel-ucode/

rm -f %{buildroot}/usr/lib/firmware/intel-ucode/0f*
tar -axf %{SOURCE20}
cp -a sound-open-firmware-binaries-1.1-apl/* %{buildroot}/usr/lib/firmware/intel

# SOF
mkdir -p %{buildroot}/usr/lib/firmware/intel/sof
cp %{SOURCE30} %{SOURCE31} %{SOURCE32} %{SOURCE33} %{SOURCE34} %{SOURCE35} %{SOURCE36} \
   %{SOURCE37} %{SOURCE38} %{SOURCE39} %{SOURCE40} %{SOURCE41} %{SOURCE42} %{SOURCE43} \
     %{buildroot}/usr/lib/firmware/intel/sof/

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

mkdir -p intel-qat-cpio/usr/lib/firmware/
cp -a %{buildroot}/usr/lib/firmware/qat_*  intel-qat-cpio/usr/lib/firmware/
(
  cd intel-qat-cpio
  find . | cpio --create --format=newc \
    | xz --check=crc32 --lzma2=dict=512KiB > %{buildroot}/usr/lib/initrd.d/qat-firmware.cpio.xz
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

# these are in alsa-firmware instead
%exclude /usr/lib/aica_firmware.bin
%exclude /usr/lib/asihpi/dsp5000.bin
%exclude /usr/lib/asihpi/dsp6200.bin
%exclude /usr/lib/asihpi/dsp6205.bin
%exclude /usr/lib/asihpi/dsp6400.bin
%exclude /usr/lib/asihpi/dsp6600.bin
%exclude /usr/lib/asihpi/dsp8700.bin
%exclude /usr/lib/asihpi/dsp8900.bin
%exclude /usr/lib/cs46xx/ba1
%exclude /usr/lib/cs46xx/cwc4630
%exclude /usr/lib/cs46xx/cwcasync
%exclude /usr/lib/cs46xx/cwcbinhack
%exclude /usr/lib/cs46xx/cwcdma
%exclude /usr/lib/cs46xx/cwcsnoop
%exclude /usr/lib/ctefx-desktop.bin
%exclude /usr/lib/ctefx-r3di.bin
%exclude /usr/lib/ctefx.bin
%exclude /usr/lib/ctspeq.bin
%exclude /usr/lib/digiface_firmware.bin
%exclude /usr/lib/digiface_firmware_rev11.bin
%exclude /usr/lib/ea/*
%exclude /usr/lib/emu/*
%exclude /usr/lib/ess/maestro3_assp_kernel.fw
%exclude /usr/lib/ess/maestro3_assp_minisrc.fw
%exclude /usr/lib/korg/k1212.dsp
%exclude /usr/lib/mixart/miXart8.elf
%exclude /usr/lib/mixart/miXart8.xlx
%exclude /usr/lib/mixart/miXart8AES.xlx
%exclude /usr/lib/multiface_firmware.bin
%exclude /usr/lib/multiface_firmware_rev11.bin
%exclude /usr/lib/pcxhr/*
%exclude /usr/lib/rpm_firmware.bin
%exclude /usr/lib/sb16/alaw_main.csp
%exclude /usr/lib/sb16/ima_adpcm_capture.csp
%exclude /usr/lib/sb16/ima_adpcm_init.csp
%exclude /usr/lib/sb16/ima_adpcm_playback.csp
%exclude /usr/lib/sb16/mulaw_main.csp
%exclude /usr/lib/turtlebeach/msndinit.bin
%exclude /usr/lib/turtlebeach/msndperm.bin
%exclude /usr/lib/turtlebeach/pndsperm.bin
%exclude /usr/lib/turtlebeach/pndspini.bin
%exclude /usr/lib/vx/*
%exclude /usr/lib/yamaha/*

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

%files qat-cpio
%defattr(-,root,root,-)
/usr/lib/initrd.d/qat-firmware.cpio.xz

%files ucode-cpio
%defattr(-,root,root,-)
/usr/lib/initrd.d/00-intel-ucode.cpio
