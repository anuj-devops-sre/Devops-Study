Topic: Linux Basics

Sabse pehle samjho:

1. Linux Kya Hai?

Linux ek:

Operating System hai
open-source hai
server world ka king hai

Most:

cloud servers
Kubernetes nodes
Docker hosts
DevOps systems

Linux par run karte hain.

2. Linux Kya Karta Hai?

Linux:

hardware manage karta hai
software run karta hai
memory manage karta hai
users manage karta hai
files manage karta hai
processes run karta hai

Simple words:
Linux computer/server ko control karta hai.

3. DevOps Me Linux Kyu Important Hai?

Because DevOps engineers:

servers manage karte hain
logs check karte hain
deployments karte hain
automation scripts likhte hain
troubleshooting karte hain

Aur ye sab mostly Linux me hota hai.

4. Linux Kaise Kaam Karta Hai?

Basic architecture:

User
 ↓
Shell (Bash)
 ↓
Kernel
 ↓
Hardware
Kernel

Linux ka brain.

Ye:

CPU
RAM
Disk
Network

manage karta hai.

Shell

User aur Linux ke beech command interface.

Example:

ls
pwd
mkdir
5. Important Linux Components
File System

Sab kuch file hota hai.

Examples:

/home
/etc
/var
/tmp
Users

Linux multi-user system hai.

Examples:

root
ubuntu
anuj
Processes

Running programs/processes.

Example:

nginx
docker
ssh
6. First Basic Commands
pwd

Present working directory.

pwd

Example output:

/home/ubuntu
ls

Files/folders dikhata hai.

ls

Detailed:

ls -l

Hidden files:

ls -a
cd

Directory change.

cd /home

Back:

cd ..

Home:

cd ~
mkdir

Folder create.

mkdir devops
touch

File create.

touch notes.txt
rm

Delete file.

rm notes.txt

Delete folder:

rm -r devops
cp

Copy files.

cp file1.txt file2.txt
mv

Move/rename.

Rename:

mv old.txt new.txt

Move:

mv file.txt /home/ubuntu/
7. Hands-on Practice (IMPORTANT)

Practice these commands yourself:

pwd
ls
mkdir linux-practice
cd linux-practice
touch notes.txt
ls -l
cp notes.txt copy.txt
mv copy.txt renamed.txt
rm renamed.txt
8. Real-World DevOps Example

Suppose:

logs check karne hain
config file edit karni hai
deployment folder me jana hai

Tab ye commands daily use hongi.

Example:

cd /var/log
ls
9. Interview Questions
Q1. Linux kya hai?

Operating system.

Q2. pwd command kya karta hai?

Current directory path dikhata hai.

Q3. ls -a kya karta hai?

Hidden files bhi show karta hai.

Q4. Difference between cp and mv?
cp → copy
mv → move/rename
10. Today's Task
Task 1

Ubuntu install karo:

VirtualBox OR
WSL2
Task 2

Commands practice karo 20–30 mins.

Task 3

GitHub Notes Push

Repo structure:

linux/
 └── day1-linux-basics.md
11. Tomorrow We Learn
Linux File System
/etc
/var
/home
/bin
/root
/tmp

AND:

File Permissions
chmod
chown

Ye bahut important topic hai 🔥
