#!/bin/zsh -xe
ScriptDir="$(dirname $(readlink -f $0))"

# Download links:
readonly ArchLinuxARM_dl_host='http://os.archlinuxarm.org/os'
readonly ArchLinuxARM_dl_rpi1='ArchLinuxARM-rpi-latest.tar.gz'
readonly ArchLinuxARM_dl_rpi2='ArchLinuxARM-rpi-2-latest.tar.gz'
readonly ArchLinuxARM_dl_rpi3='ArchLinuxARM-rpi-3-latest.tar.gz'

# Please select the correct image here:
readonly ArchLinuxARM_image="${ArchLinuxARM_dl_rpi1}"

# readonly WorkingDirectory="${ScriptDir}/working"
readonly WorkingDirectory="${ScriptDir}/../working"
mkdir "${WorkingDirectory}" -p
cd "${WorkingDirectory}"

readonly ArchLinuxARM_downurl="${ArchLinuxARM_dl_host}/${ArchLinuxARM_image}"
readonly ArchLinuxARM_imgfile="${ArchLinuxARM_image}"


downloadImage() {
  if [[ ! -f "${ArchLinuxARM_imgfile}" ]]; then
    wget "${ArchLinuxARM_downurl}" -O "${ArchLinuxARM_imgfile}"
  fi
}

extractImage() {
  # Keep the latest working directory to prevent some cries
  if [[ -d "root" ]]; then
    rm -rf        "root_latest"
    mv    "root"  "root_latest"
  fi
  mkdir "root"

  bsdtar -xpf "${ArchLinuxARM_imgfile}" -C "root"
}


downloadQemu() {
  hash "apt-get" && apt-get install qemu-arm-static
  hash "yaourt"  && sudo -u $SUDO_USER yaourt -S --noconfirm --needed binfmt-support qemu-user-static
}

prepareInstall() {
  # Install qemu into the chroot
  cp $(which qemu-arm-static) "root/usr/bin"

  # Allow access from chroot to our repository
  cp -Tr "${ScriptDir}" "root/repository"
  trap 'rm -rf root/repository' EXIT

  arch-chroot "root" /usr/bin/qemu-arm-static /usr/bin/bash "/repository/archlinux_prepare_intochroot.sh"
}

prepareDisk() {
  Disk="$1"

  # Umount…
  umount -f ${Disk}? || /bin/true
  sync ; sleep 1

  # Create /boot (100M), / (the rest)
  (
    echo o
    echo n ; echo p ; echo 1 ; echo ; echo +100M
    echo t ; echo c
    echo n ; echo p ; echo 2 ;  echo ; echo

    echo w ;
  ) | fdisk "${Disk}"
  sync ; sleep 1

  mkfs.vfat    "${Disk}1"
  sync ; sleep 1
  mkfs.ext4 -F "${Disk}2"
  sync ; sleep 1
}

copyToDisk() {
  Disk="$1"

  # Umount…
  umount -f ${Disk}? || /bin/true

  mkdir -p          "mount_boot"
  mount "${Disk}1"  "mount_boot"
  mkdir -p          "mount_root"
  mount "${Disk}2"  "mount_root"

  rsync --aAXv "root/boot/*"  "mount_boot"
  rsync --aAXv "root/*"       "mount_root"
  sync ; sleep 1

  umount "mount_boot" "mount_root"
  sync ; sleep 1
}


# Check if launched with sudo
if [[ -z "$SUDO_USER" ]]; then
  echo "This script should be executed with sudo."
  exit 1
fi


downloadImage
downloadQemu
extractImage
prepareInstall

# prepareDisk
# copyToDisk
