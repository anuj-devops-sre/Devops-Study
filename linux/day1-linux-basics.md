# Recommended DevOps Study Repository Structure

```text
Devops-Study/
├── linux/
│   ├── day1-linux-basics.md
│   ├── day2-filesystem-permissions.md
│   ├── day3-process-management-logs.md
│   ├── day4-users-groups.md
│   ├── day5-ssh-scp.md
│   ├── day6-package-management-services.md
│   ├── day7-system-monitoring.md
│   ├── day8-networking-commands.md
│   ├── day9-file-processing.md
│   └── day10-cron-automation.md
│
├── networking/
│   ├── day1-osi-model.md
│   ├── day2-tcp-ip-dns.md
│   ├── day3-http-https-loadbalancer.md
│   ├── day4-cidr-subnet-nat-firewall.md
│   └── day5-nginx-reverse-proxy.md
│
├── git/
├── docker/
├── aws/
├── terraform/
├── kubernetes/
├── monitoring/
├── security/
└── projects/
```

---

# Detailed Notes Format (Important)

All future notes will include:

* What is it?
* Why do we use it?
* How does it work?
* Command meaning
* Option breakdown
* Syntax
* Example output
* Real-world DevOps usage
* Production troubleshooting
* Interview questions
* Hands-on practice

Example format:

```markdown
# ps aux

## Meaning
ps = process status

## Purpose
Shows all running processes.

## Breakdown
- a = all users processes
- u = user-oriented format
- x = background processes

## Example
ps aux

## Output Fields
USER = process owner
PID = process ID
%CPU = CPU usage
%MEM = memory usage

## Real DevOps Usage
Find nginx process:
ps aux | grep nginx

## Troubleshooting
Find high CPU process:
ps aux --sort=-%cpu | head

## Important Notes
Used heavily in production troubleshooting.
```

---

# DevOps Study Repository Structure

```text
Devops-Study/
├── linux/
│   └── day1-linux-basics.md
├── networking/
├── git/
├── docker/
├── aws/
├── terraform/
├── kubernetes/
├── monitoring/
└── projects/
```

---

# File: linux/day1-linux-basics.md

````markdown
# Day 1 - Linux Basics

# What is Linux?

Linux is an open-source operating system widely used in servers, cloud computing, DevOps, and containers.

---

# Why Linux is Important in DevOps?

DevOps engineers use Linux for:
- Server management
- Automation
- Monitoring
- Deployments
- Troubleshooting

Most cloud servers run on Linux.

---

# Linux Architecture

User → Shell → Kernel → Hardware

## Kernel
The core part of Linux that manages:
- CPU
- Memory
- Processes
- Devices

## Shell
Command-line interface used to interact with Linux.

Example:
```bash
ls
pwd
mkdir
```

---

# Basic Linux Commands

## pwd
Shows current directory.

```bash
pwd
```

---

## ls
Lists files and folders.

```bash
ls
ls -l
ls -a
```

---

## cd
Changes directory.

```bash
cd /home
cd ..
cd ~
```

---

## mkdir
Creates folder.

```bash
mkdir devops
```

---

## touch
Creates file.

```bash
touch notes.txt
```

---

## rm
Deletes files/folders.

```bash
rm notes.txt
rm -r devops
```

---

## cp
Copies files.

```bash
cp file1.txt file2.txt
```

---

## mv
Moves or renames files.

```bash
mv old.txt new.txt
```

---

# Hands-on Practice

```bash
pwd
ls
mkdir linux-practice
cd linux-practice
touch notes.txt
ls -l
cp notes.txt copy.txt
mv copy.txt renamed.txt
rm renamed.txt
```

---

# Real-world DevOps Usage

Linux commands are used for:
- Checking logs
- Managing servers
- Deploying applications
- Editing configuration files

Example:

```bash
cd /var/log
ls
```

---

# Interview Questions

## What is Linux?
Linux is an open-source operating system.

## What does pwd do?
Shows present working directory.

## Difference between cp and mv?
- cp = copy
- mv = move/rename

---

# Summary

Today we learned:
- Linux basics
- Linux architecture
- Basic commands
- Hands-on practice
````

# DevOps Study Notes (Linux + Networking)

These notes are designed for:

* quick revision
* interview preparation
* production troubleshooting
* mid-level DevOps daily usage

---

# Linux Notes

## Day 1 — Linux Basics

### What is Linux?

Linux is an open-source operating system widely used in cloud servers, DevOps, Docker, and Kubernetes.

---

# pwd

## Meaning

pwd = present working directory

## Purpose

Shows current directory path.

## Example

```bash
pwd
```

## Example Output

```text
/home/ubuntu
```

## Real DevOps Usage

Used during deployments and log navigation.

---

# ls

## Purpose

Lists files and folders.

## Commands

```bash
ls
ls -l
ls -a
```

## Breakdown

* -l = long listing format
* -a = hidden files

---

# chmod

## Meaning

chmod = change mode

## Purpose

Changes file permissions.

## Example

```bash
chmod 755 deploy.sh
```

## Breakdown

7 = rwx
5 = r-x
5 = r-x

## Real DevOps Usage

Used for deployment scripts.

---

# ps aux

## Meaning

ps = process status

## Purpose

Shows running processes.

## Breakdown

* a = all users
* u = user format
* x = background processes

## Example

```bash
ps aux
```

## Real DevOps Usage

```bash
ps aux | grep nginx
```

---

# tail -f

## Purpose

Shows live logs.

## Example

```bash
tail -f /var/log/syslog
```

## Real DevOps Usage

Production log monitoring.

---

# SSH

## Meaning

SSH = Secure Shell

## Purpose

Remote server access.

## Example

```bash
ssh ubuntu@server-ip
```

---

# SCP

## Meaning

SCP = Secure Copy

## Example

```bash
scp file.txt user@server:/tmp
```

---

# df -h

## Meaning

df = disk filesystem

## Purpose

Shows disk usage.

## Example

```bash
df -h
```

---

# free -h

## Purpose

Shows memory usage.

## Example

```bash
free -h
```

---

# curl

## Meaning

Client URL

## Purpose

Sends HTTP requests.

## Example

```bash
curl google.com
```

---

# Networking Notes

## OSI Model

### Meaning

OSI = Open Systems Interconnection

### Purpose

Networking communication model.

---

# TCP

## Meaning

TCP = Transmission Control Protocol

## Purpose

Reliable communication.

---

# UDP

## Meaning

UDP = User Datagram Protocol

## Purpose

Fast communication.

---

# DNS

## Meaning

DNS = Domain Name System

## Purpose

Converts domain names to IP addresses.

---

# dig

## Meaning

Domain Information Groper

## Example

```bash
dig google.com
```

---

# HTTP

## Meaning

HTTP = HyperText Transfer Protocol

## Purpose

Client-server communication.

---

# HTTPS

## Purpose

Encrypted communication using SSL/TLS.

---

# CIDR

## Meaning

CIDR = Classless Inter-Domain Routing

## Example

```text
192.168.1.0/24
```

---

# NAT

## Meaning

NAT = Network Address Translation

## Purpose

Allows private servers internet access.

---

# Nginx

## Purpose

Web server + reverse proxy + load balancer.

---

# proxy_pass

## Purpose

Forwards traffic to backend application.

## Example

```nginx
proxy_pass http://localhost:3000;
```

---

# Important Production Commands

```bash
ps aux
htop
df -h
free -h
tail -f /var/log/syslog
curl -I google.com
ss -tulnp
systemctl status nginx
nginx -t
```
