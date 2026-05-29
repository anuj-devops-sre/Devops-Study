# 🐧 LINUX SRE MASTER STUDY GUIDE (Day 1 - Day 18)

This is a comprehensive guide covering everything from Linux fundamentals to advanced system administration and container internals, specifically tailored for SRE and Platform Engineer roles.

---

## 📅 Day 1: Architecture & Shell Basics
- **Architecture**: Kernel, Shell, User Space vs. Kernel Space.
- **Shells**: Bash (Standard), Zsh (Modern), Sh.
- **Navigation**: `ls`, `cd`, `pwd`, `mkdir`, `rm`, `mv`, `cp`.

## 📅 Day 2: File System & Permissions
- **FHS (File System Hierarchy)**: `/etc` (Config), `/var/log` (Logs), `/bin` (Executables), `/root`, `/home`.
- **Permissions**: Read (4), Write (2), Execute (1). `chmod`, `chown`, `chgrp`.
- **Special Permissions**: Sticky Bit, SUID, SGID.

## 📅 Day 3: User & Group Management
- **Users**: `/etc/passwd`. `useradd`, `usermod`, `userdel`.
- **Groups**: `/etc/group`. `groupadd`.
- **Sudoers**: `/etc/sudoers`. Giving administrative access safely.

## 📅 Day 4: Package Management
- **APT (Debian/Ubuntu)**: `apt update`, `apt install`, `apt upgrade`.
- **YUM/DNF (RHEL/CentOS)**: `yum install`, `dnf update`.
- **Source Compilation**: `make`, `make install`.

## 📅 Day 5: Process Management
- **Monitoring**: `ps aux`, `top`, `htop`.
- **Control**: `kill -9` (Force), `kill -15` (Graceful), `nice`, `renice`.
- **Background/Foreground**: `&`, `bg`, `fg`, `jobs`.

## 📅 Day 6: Systemd & Init Systems
- **Systemd**: The modern init system.
- **Commands**: `systemctl start/stop/restart/status`, `systemctl enable/disable`.
- **Journals**: `journalctl -u nginx -f`.

## 📅 Day 7: Storage & Disk Management
- **Disk Usage**: `df -h` (Filesystem), `du -sh` (Directory size).
- **LVM**: Physical Volumes, Volume Groups, Logical Volumes.
- **Partitions**: `fdisk`, `lsblk`, `mount`, `/etc/fstab`.

## 📅 Day 8: Networking Fundamentals
- **Interface**: `ip addr`, `ifconfig` (Legacy).
- **Connectivity**: `ping`, `traceroute`, `telnet`, `nc` (Netcat).
- **DNS/Ports**: `nslookup`, `dig`, `netstat -tulpn`, `ss`.

## 📅 Day 9: Log Management & Rotation
- **Central Logs**: `/var/log/syslog`, `/var/log/auth.log`.
- **Logrotate**: Managing disk space by compressing/deleting old logs.

## 📅 Day 10-11: Shell Scripting (Basics to Advanced)
- **Variables**: `NAME="Anuj"`.
- **Loops**: `for`, `while`.
- **Conditionals**: `if-else`, `case`.
- **Functions**: Reusable code blocks.
- **Automation**: Automating backups and cleanup scripts.

## 📅 Day 12: CRON & Job Scheduling
- **Crontab**: `* * * * * command`. (Minute, Hour, Day, Month, Weekday).
- **Systemd Timers**: The modern alternative to Cron.

## 📅 Day 13: Kernel & Boot Process
- **Kernel**: `uname -a`, `lsmod`, `insmod`.
- **Boot**: BIOS/UEFI -> GRUB -> Kernel -> Init (Systemd).

## 📅 Day 14: Security & Firewalls
- **Firewalls**: `ufw` (Simple), `iptables` (Advanced), `firewalld`.
- **Hardening**: Disabling Root SSH, using Fail2Ban.

## 📅 Day 15: Performance Tuning
- **CPU**: `lscpu`, `uptime` (Load average).
- **RAM**: `free -m`, `vmstat`.
- **I/O**: `iostat`, `iotop`.

## 📅 Day 16: Real-world Troubleshooting
- **Scenario**: "Website is slow." -> Check CPU/RAM -> Check Logs -> Check Network.
- **Scenario**: "Disk Full." -> `du -ah / | sort -rh | head -n 20`.

## 📅 Day 17: SSH Hardening & Bastion
- **SSH Config**: `/etc/ssh/sshd_config`.
- **Bastion Hosts**: Secure entry point for private networks.

## 📅 Day 18: Linux for Containers
- **Cgroups**: Resource limiting (CPU/RAM).
- **Namespaces**: Isolation (Network, PID, Mount).
- **OverlayFS**: The storage driver for Docker.
