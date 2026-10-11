# PYNQ 2.7 for Zedboard
> [!NOTE]  
> This guide assumes that there is always enough performance available to build PYNQ. Therefore any hardware/performance requirements are omitted. For the hardware requirements please check the corresponding documentation of each used tool. In general anything above 16GB RAM and 250GB Free DiskSpace should be plenty to build and install everything needed.

> [!IMPORTANT]  
> The build chain for PYNQ is very fragile, it highly recommended to create a fresh Linux-Instance to install and build PYNQ with.

## Pre-Requirements
### Binary Downloads
Download the following files. We will need them later:
- `ubuntu-18.04-server-cloudimg-amd64-wsl.rootfs.tar.gz ` from [Ubuntu 18.04 LTS (Bionic Beaver) Release Download Page](https://cloud-images.ubuntu.com/releases/bionic/release/)
- `Vitis Core Development Kit - 2020.2 - Nov 24,2020` from [Adaptive SoCs & FPGA Design Tools Downloads - 2020.2](https://www.amd.com/en/support/downloads/adaptive-socs-and-fpgas/development-tools/2020-2.html)
- `PetaLinux 2020.2 Installer¹` from [Adaptive SoCs & FPGA Embedded Software Downloads](https://www.amd.com/en/support/downloads/adaptive-socs-and-fpgas/embedded-software.html)
- `v2.7 ARM root filesystem` aka. `focal.arm.2.7.0_2021_11_17.tar.gz` from the _Previous image build files_ section at the bottom of [PYNQ.io Boards and images](https://www.pynq.io/index.html#boards)
- `ZED BSP` with [Version: `2020.2`, ProductFamily: `Avnet Digital`] from [Adaptive SoCs & FPGA Embedded Software Downloads](https://www.amd.com/en/support/downloads/adaptive-socs-and-fpgas/embedded-software.html#tabs-13aaba6de8-item-3e5066a8e9-tab)

> [!NOTE]
> It is recommended to download these files with the Host-System and Copy/Move them over to the Linux Instance. However, doing so is entirely optional. You can also download them directly into the Linux instance. There is no technical reason for doing one way over the other.

### Setup Host Environment
#### Windows Subsystem for Linux (WSL) - Windows Host
Since Ubuntu 18.04 is not officially supported WSL2-Linux-Distribution anymore, it has to be installed manually.

1. Get `ubuntu-18.04-server-cloudimg-amd64-wsl.rootfs.tar.gz ` from [Ubuntu 18.04 LTS (Bionic Beaver) Release Download Page](https://cloud-images.ubuntu.com/releases/bionic/release/)
2. Fill in and execute the following in your Powershell Terminal:
```bash
mkdir C:\WSL\Ubuntu-18.04
wsl --import Ubuntu-18.04 C:\WSL\Ubuntu-18.04 C:\Your\Path\to\bionic-server-cloudimg-amd64-wsl.rootfs.tar.gz
wsl -d Ubuntu-18.04
```
It may take a while to start up but if everything was successful a Linux terminal with logged in `root` user should show up in your Powershell Terminal.

3. Run the following command to check the OS version and verify it is the correct one.
```bash
cat /etc/os-release
```

#### Configuring WSL Linux instance
Since always being `root` user is a bad practice and PYNQ is checking for not being `root` user, it needs to be changed.

1. Add a new user to the Linux instance.
```bash
adduser pynqdev
usermod -aG sudo pynqdev
su - pynqdev
```

2. Add the new user as default log-in user via `/etc/wsl.conf`. While we do this we also enable `systemd` so QEMU can emulate the ARM processor later in the build.
```bash
cat <<EOF > /etc/wsl.conf
[boot]
systemd=true

[user]
default=pynqdev
EOF
```
3. PYNQ expects the default shell to be `bash` and not `dash`. Execute the following and a screen will pop up. Select `No` so `dash` is no longer the default shell.
```bash
sudo dpkg-reconfigure dash
```

> [!WARNING]  
> Disabling the password check for `sudo` interactions in Linux is considered an extreme safety hazard! Make sure to use this on isolated & disposable machines only!

4. (**Optional!**) Disable password check when using sudo.
- Temporary: `echo "pynqdev ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/pynqdev`
- Forever:
```bash
sudo visudo
# A Text-Editor should open in the terminal. add the following line at the end of the file
pynqdev ALL=(ALL) NOPASSWD: ALL
```

5. Restart your WSL-Instance.
```bash
# WARNING: Shuts down all running WSL instances!
wsl --shutdown 
 # Login + StartUp
wsl -d Ubuntu-18.04
```

#### Additional Configuration
> [!NOTE]  
> The following configuration(s) may or may not be important. If you run into trouble while installing/executing the toolchain check back into this section.

##### sock.connect(sa) can not be established/hangs forever 
**MTU mismatch:**
A common issue with WSL and older not officially supported Linux Distributions is a mismatch in the MTU (Maximum Transmission Unit) package size. WSL creates a virtual router and other networking components through which the Linux distribution is accessing the internet. Sometimes the Package size is not correct leading to either timeout connections or silent dropping of packages. To fix this verify the package size:

Execute: `ping -c 4 -M do -s 1472 8.8.8.8` in the Linux-Terminal.

This command will send **4** `ping` requests which are **not fragmented** (`-M do`) and have a **size of 1472 bytes** to [Google Public DNS](https://developers.google.com/speed/public-dns). Adding the mandatory 20-byte IP header and 8 byte ICMP Header is done automatically when executing `ping`, leading to _1500_ bytes in total packet size which is the maximum for Ethernet networks.

If this returns something along the lines of `Frag needed and DF set (mtu = 1460) ping: local error: Message too long, mtu=1460` then your MTU settings are wrong and need to be adjusted. For example: `sudo ip link set dev eth0 mtu 1460`. This forces your virtual network connector to use the right MTU size.

**IPv6 routing issues in WSL2**
Specially for older Linux distributions, sometimes the IPv6 routing is silently dropped by the WSL-Network-Router. Usually you can safely disable any IPv6 connections. This forces Linux to default back to IPv4 routing which works flawlessly.

Execute in the Linux Terminal:
```
sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1
```

##### Docker & QEMU
PYNQ uses QEMU to update the ARM based operating system. WSL depends on a Container Engine for this. Usually [Docker](https://www.docker.com/). The following command updates necessary Docker-Components so WSL can utilize QEMU with ARM. To be executed in a `PowerShell`!
```bash
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
```

##### Unable to locate package zlib1g:i386
This happens because Ubuntu 64-bit architecture has no 32-bit architecture packages enabled by default. The fix is to simply add the missing packages and update.
```bash
sudo dpkg --add-architecture i386
sudo apt-get update
```

## Install the Toolchain
### PYNQ 2.7
#### Downloading PYNQ 2.7
Installing PYNQ and checking out v2.7 is straightforward, since it is a git repository. 
```bash
# This clones PYNQ to your current directory
git clone https://github.com/Xilinx/PYNQ.git
cd PYNQ
git checkout v2.7.0 
```

#### Update setup_host.sh and run it
Since some of the network requests never ever resolve due to dead endpoints, we have to change the `/PYNQ/sdbuild/scripts/setup_host.sh` file.

1. Comment out the following line by putting a `#` in front of it: `sudo add-apt-repository -y ppa:ubuntu-toolchain-r/ppa`
2. Execute the following:
```bash
cd PYNQ/sdbuild/scripts
sudo bash setup_host.sh
```
> [!IMPORTANT]  
> If the script hangs too long especially on network tasks, check out the earlier defined additional configuration section for further details.

### Xilinx 2020.2
> [!NOTE]  
> The Installer may complain that you have the wrong Ubuntu/OS version. This happens due to the installer checking OS version against hardcoded values. For example: A Ubuntu 18.04.04 would be valid and a Ubuntu 18.04.06 wouldn't. However, the underlying filesystem etc. is identical and that is what the Xilinx Tool-Chain needs/expects. So you can safely ignore this warning.

1. Get `Vitis Core Development Kit - 2020.2 - Nov 24,2020` from [Adaptive SoCs & FPGA Design Tools Downloads - 2020.2](https://www.amd.com/en/support/downloads/adaptive-socs-and-fpgas/development-tools/2020-2.html).
2. Navigate to the location the Development Kit is located after the download by using `cd` commands.
3. Execute the following:
```bash
# Create the Standard Xilinx folder
sudo mkdir -p /tools/Xilinx
# Allow the none root user to own the folder for no access conflicts when installing
sudo chown -R pynqdev:pynqdev /tools/Xilinx
# Unpack/Extract the downloaded archive

# make the xilinx installer executable and its other scripts components executable
DAS HIER MUSS GEÄNDERT WERDEN!!!!!!!!!!!!!!!! -> chmod -R +x . -> das hier mach alle files/order etc. ausführbar. ggf. gibt es da einen besseren Befehl für.
chmod +x Xilinx_Unified_2020.2_*_Lin64.bin
# execute the installer
./xsetup
```
You should now be able to install Vitis which includes everything we need for PYNQ to build. The following is recommended:
1. When able to define the path in which the installer should install Vitis make sure it points to the default and correct path `/tools/Xilinx`
2. When asked which installation preset the installer should use, select `Vitis`.
3. When asked which parts to install you can safely uncheck the following:
    - Matlab and Simulink Addon
    - Any Device or Device Family that is not a `7 Series` Device (Uncheck UltraScale, UltraScale+, Versal ACAP)
    - Alveo and Xilinx edge acceleration
    - **Leave `SoCs` and `7 Series` checked! Both is needed for the Zedboard!**

#### Additional Infos for installing Xilinx Tools.
> [!NOTE]  
> The following information may or may not be important. If you run into trouble while installing/executing the toolchain check back into this section.

##### y2k22 Bug
The bug is documented and explained [here](https://adaptivesupport.amd.com/s/article/76960?language=en_US). Please follow the directions from the official documentation on this issue.

##### Missing Files/Directories when starting Vivado
You may encounter a `Vivado 2020.2 Error: application-specific initialization failed: couldn't load file "librdi_commontasks.so": libtinfo.so.5: cannot open shared object file: No such file or directory`. If that happens just execute/download the missing packages with: `sudo apt update && sudo apt install libtinfo5 libncurses5 -y`. It installs the missing dependencies.

### Petalinux 2020.2
1. Get `PetaLinux 2020.2 Installer¹` from [Adaptive SoCs & FPGA Embedded Software Downloads](https://www.amd.com/en/support/downloads/adaptive-socs-and-fpgas/embedded-software.html)
2. Navigate to the location the Petalinux Installer is located after the download by using `cd` commands.
3. Execute the following:
```bash
# Create the Standard Petalinux folder
sudo mkdir -p /tools/petalinux/2020.2
# Allow the none root user to own the folder for no access conflicts when installing
sudo chown -R pynqdev:pynqdev /tools/petalinux/
sudo chown -R pynqdev:pynqdev /tools/petalinux/2020.2
# make the petalinux installer executable 
chmod +x petalinux-v2020.2-final-installer.run
# execute the installer
./petalinux-v2020.2-final-installer.run --dir /tools/petalinux/2020.2
```

### Verify the installation
1. PYNQ already verified due to the `setup_host.sh` script being successful.
2. Source Xilinx Settings -> `source /tools/Xilinx/Vitis/2020.2/settings64.sh`
3. Source Petalinux Settings -> `source /tools/petalinux/2020.2/settings.sh`

### Quality of Life Configuration
By default the source commands are not loaded for every new terminal session. You can adjust the `bashrc` file to source automatically for every new Terminal session.
```bash
# Open bashrc file with a texteditor
nano ~/.bashrc
# add these two lines at the end of the file.
source /tools/Xilinx/Vitis/2020.2/settings64.sh
source /tools/petalinux/2020.2/settings.sh
```
## (Attempting to) Build PYNQ 2.7
### Update build scripts/files
#### Skip original build.sh
Navigate to `` and update the entire file with:
```bash
#!/bin/bash
echo "Skipping global build.sh"
exit 0
```
This skips the `build.sh` file but exits it cleanly so depending processes assume it went fine.


### Delete any Boards that are not Zedboard
Navigate to `/PYNQ/boards/`. In this folder you will find multiple boards and other components. Delete everything except for: `ip` and `sw_repo`.

To prevent the Toolchain from re-downloading files that we changed or deleted a dummy git commit has to be done.
Execute:
```bash
# create a dummy git user
git config --global user.email "pynqdev@local.host"
git config --global user.name "pynqdev"

# add the dummy commit
cd ~/PYNQ
git add -u boards/
git commit -m "Permanently removed factory boards"
```
### Define Zedboard.spec & add correct Board-Support-Package (BSP)
Each PYNQ has to be build for each board individually. For this a `.spec` file and corresponding `.bsp` file is used. 

For the Zedboard a `.spec` file is provided [here](./Zedboard.spec). Make sure it is placed at `/PYNQ/boards/Zedboard/Zedboard.spec`. The corresponding `ZED BSP` with [Version: `2020.2`, ProductFamily: `Avnet Digital`] from [Adaptive SoCs & FPGA Embedded Software Downloads](https://www.amd.com/en/support/downloads/adaptive-socs-and-fpgas/embedded-software.html#tabs-13aaba6de8-item-3e5066a8e9-tab) also needs to be placed in this directory!

### Add prebuild ARM Filesystem
Navigate to `/PYNQ/sdbuild` and place `focal.arm.2.7.0_2021_11_17.tar.gz` downloaded earlier at the same location.

### Attempt to build ones and wait for it to fail
To execute the build of PYNQ 2.7, stay in `/PYNQ/sdbuild` and execute `make PREBUILT=~/PYNQ/sdbuild/focal.arm.2.7.0_2021_11_17.tar.gz BOARDS=Zedboard`.

It is supposed to crash. Not literally but because Github changed... **BEGRÜNDUNG NOCH EINBAUEN** two dependencies for `wictools` can not be found. 

Execute the following:
```bash
cd ~/PYNQ/sdbuild/build/Zedboard/petalinux_project/build/downloads/git2

rm -rf github.com.lz4.lz4.git
git clone --bare https://github.com/lz4/lz4.git github.com.lz4.lz4.git
cd github.com.lz4.lz4.git
git branch master fdf2ef5809ca875c454510610764d9125ef2ebbd
cd ..

rm -rf github.com.intel.bmap-tools
git clone --bare https://github.com/intel/bmap-tools.git github.com.intel.bmap-tools
cd github.com.intel.bmap-tools
git branch master db7087b883bf52cbff063ad17a41cc1cbb85104d
```

Now we only have to clean the `wic-tools` state and re-run the build of this specific part of the tool-chain.
```bash
cd ~/PYNQ/sdbuild/build/Zedboard/petalinux_project
petalinux-build -c wic-tools -x cleansstate
petalinux-build -c wic-tools
```

Navigate back to the `sdbuild` directory and resume the build.
```bash
cd ~/PYNQ/sdbuild
make PREBUILT=~/PYNQ/sdbuild/focal.arm.2.7.0_2021_11_17.tar.gz BOARDS=Zedboard
```

The build should finish now and in the `sdbuild/output` directory, you should find a `Zedboard-2.7.0.img` file. Which you can flash to your SD-Card.

## Flashing to SD-Card
For this we went with [Rufus](https://rufus.ie/en/).

1. Insert your SD-Card and make sure you can access it.
2. Download and Start Rufus.
3. When Rufus pops up:
    1. Select your Device -> Your SD-Card
    2. Select the PYNQ `.img` File by hitting the `SELECT` Button in the Boot selection.
    3. Choose your build PYNQ `.img` file.
    4. The Informations below the boot selection should autofill.
    5. Hit `START` and enter `OK` the two times Rufus is warning after you hit `START`.
4. Extract the SD-Card safely from your computer.
5. Put it into the Zedboard and turn the power on it.

> [!IMPORTANT]  
> Check the Jumper-Configuration on your Zedboard before starting it. It has to be put into _"Boot from SD-Card"_-Mode. For this search for the Jumper-Array J07 to J11. The following table illustrates how to setup these 5 Jumpers for SD-Mode.

| Jumper | GND | SIG | 3V3 |
| :----: | :-: | :-: | :-: |
|  J07   |  X  |  X  |     |
|  J08   |  X  |  X  |     |
|  J09   |     |  X  |  X  |
|  J10   |     |  X  |  X  |
|  J11   |  X  |  X  |     |