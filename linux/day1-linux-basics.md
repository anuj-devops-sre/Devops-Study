**LINUX**

**COMPLETE DAILY REVISION GUIDE**

**Zero to Mid-Level**

**DevOps Engineer | Platform Engineer | SRE Engineer**

Every Command with Explanation + Why We Use It

# **1\. Linux Fundamentals & Filesystem**

Linux ek open-source operating system hai jo servers, cloud, containers aur embedded systems mein sabse zyada use hota hai. DevOps/SRE engineers ke liye Linux ki deep understanding zaroori hai kyunki production infrastructure mostly Linux-based hoti hai.

## **1.1 Linux Directory Structure (FHS - Filesystem Hierarchy Standard)**

| **Command / Syntax** | **Kya Karta Hai**                                         | **Kyu Use Karte Hain**              |
| -------------------- | --------------------------------------------------------- | ----------------------------------- |
| **/**                | Root directory - poora filesystem yahan se start hota hai | Sab kuch yahan se hi begin hota hai |
| **/bin**             | Essential binary commands (ls, cp, mv, cat)               | Basic commands jo har user use kare |
| **/sbin**            | System binaries (root only: fdisk, reboot, ifconfig)      | System administration commands      |
| **/etc**             | Configuration files (nginx.conf, passwd, hosts)           | Saari configs yahan store hoti hain |
| **/home**            | Normal users ke home directories (/home/john)             | User-specific files aur settings    |
| **/root**            | Root user ka home directory                               | Superuser ka personal directory     |
| **/var**             | Variable data: logs, spool, cache (/var/log)              | Dynamically changing data           |
| **/tmp**             | Temporary files (reboot pe delete ho jaate hain)          | Short-lived temporary data          |
| **/usr**             | User programs, libraries, documentation                   | Installed applications yahan hain   |
| **/opt**             | Optional/third-party software (Jenkins, custom apps)      | Custom installs ke liye             |
| **/proc**            | Virtual FS for kernel/process info (/proc/cpuinfo)        | Live system information             |
| **/sys**             | Virtual FS for hardware/kernel parameters                 | Hardware aur driver info            |
| **/dev**             | Device files (sda, tty, null, zero, random)               | Hardware devices as files           |
| **/mnt**             | Mount point for manually mounted filesystems              | Temporary mounts yahan karte hain   |
| **/media**           | Mount point for removable media (USB, CD)                 | Auto-mount removable devices        |
| **/boot**            | Bootloader files (vmlinuz, initrd, grub)                  | OS boot karne ke liye files         |
| **/lib**             | Essential shared libraries (.so files)                    | Binaries ke liye libraries          |
| **/run**             | Runtime data since last boot (PIDs, sockets)              | Temporary runtime information       |

## **1.2 Navigation Commands**

| **Command / Syntax** | **Kya Karta Hai**                                         | **Kyu Use Karte Hain**             |
| -------------------- | --------------------------------------------------------- | ---------------------------------- |
| **pwd**              | Present Working Directory print karta hai                 | Current location jaanne ke liye    |
| **ls**               | Current directory ki files list karta hai                 | Files dekhne ke liye               |
| **ls -l**            | Long format: permissions, owner, size, date               | Detailed info ke liye              |
| **ls -la**           | Hidden files bhi include karta hai (. se start hone wale) | Hidden config files dekhne ke liye |
| **ls -lh**           | Human-readable size (KB, MB, GB)                          | File sizes easily padhne ke liye   |
| **ls -ltr**          | Time-sorted, reverse order (latest last)                  | Recent changes dekhne ke liye      |
| **ls -R**            | Recursively sab directories list karta hai                | Full tree dekhne ke liye           |
| **ls -ld /etc**      | Directory ki khud ki info (contents nahi)                 | Dir permissions check ke liye      |
| **cd /var/log**      | Specified path pe jaata hai                               | Directory change karne ke liye     |
| **cd ~**             | Home directory pe jaata hai                               | Quickly home jaane ke liye         |
| **cd -**             | Previous directory pe wapas jaata hai                     | Toggle between 2 dirs              |
| **cd ..**            | Parent directory pe jaata hai                             | Ek level upar jaane ke liye        |
| **cd ../../etc**     | Multiple levels upar phir navigate                        | Relative path navigation           |
| **tree**             | Directory structure tree format mein dikhata hai          | Visual folder structure            |
| **tree -L 2**        | Sirf 2 levels deep dikhata hai                            | Controlled depth view              |
| **tree -a**          | Hidden files bhi show karta hai                           | Complete tree with hidden          |

## **1.3 File Operations**

| **Command / Syntax**            | **Kya Karta Hai**                                         | **Kyu Use Karte Hain**   |
| ------------------------------- | --------------------------------------------------------- | ------------------------ |
| **touch file.txt**              | Empty file create karta hai ya timestamp update karta hai | Quickly file banana      |
| **touch -t 202401011200 f**     | Specific timestamp set karta hai                          | Timestamp manipulation   |
| **cp src.txt dst.txt**          | File copy karta hai                                       | File duplicate karna     |
| **cp -r dir1/ dir2/**           | Directory recursively copy karta hai                      | Pura folder copy karna   |
| **cp -p file1 file2**           | Permissions aur timestamps preserve karta hai             | Exact copy banana        |
| **cp -i src dst**               | Overwrite se pehle confirm maangta hai                    | Safe copy                |
| **mv old.txt new.txt**          | File rename ya move karta hai                             | Rename/move ke liye      |
| **mv \*.log /var/log/archive/** | Multiple files move karta hai                             | Bulk file movement       |
| **rm file.txt**                 | File permanently delete karta hai                         | File remove karna        |
| **rm -rf /path/to/dir**         | Directory recursively force delete (DANGEROUS!)           | Cleanup, BE CAREFUL      |
| **rm -i file.txt**              | Delete se pehle confirm maangta hai                       | Safe delete              |
| **mkdir newdir**                | New directory create karta hai                            | Folder banana            |
| **mkdir -p a/b/c/d**            | Parent dirs bhi automatically create karta hai            | Nested dirs at once      |
| **rmdir emptydir**              | Sirf empty directory delete karta hai                     | Safe dir remove          |
| **ln -s /path/to/src link**     | Symbolic (soft) link banata hai                           | Shortcut/alias banana    |
| **ln file hardlink**            | Hard link banata hai                                      | Same inode, another name |
| **stat file.txt**               | File ka inode, timestamps, permissions dikhata hai        | Detailed file metadata   |
| **file file.txt**               | File ka actual type detect karta hai                      | Binary vs text check     |
| **basename /etc/nginx.conf**    | Path se sirf filename nikalta hai                         | Scripting mein use       |
| **dirname /etc/nginx.conf**     | Path se sirf directory nikalta hai                        | Scripting mein use       |

## **1.4 File Viewing & Reading**

| **Command / Syntax**        | **Kya Karta Hai**                                 | **Kyu Use Karte Hain**          |
| --------------------------- | ------------------------------------------------- | ------------------------------- |
| **cat file.txt**            | Pura file content print karta hai                 | Small files dekhne ke liye      |
| **cat -n file.txt**         | Line numbers ke saath print karta hai             | Line reference ke liye          |
| **cat -A file.txt**         | Invisible chars (^M, \$) dikhata hai              | Windows line-ending detect      |
| **tac file.txt**            | File ko reverse order mein print karta hai        | Last lines pehle dekhna         |
| **less file.txt**           | File ko page-by-page scroll karta hai (q to quit) | Large file padhne ke liye       |
| **less +F file.txt**        | tail -f jaisa real-time follow karta hai          | Live log monitoring             |
| **more file.txt**           | Simple pager, less se purana                      | Basic paging                    |
| **head file.txt**           | File ki pehli 10 lines dikhata hai                | File start dekhne ke liye       |
| **head -n 50 file.txt**     | Pehli 50 lines dikhata hai                        | Custom line count               |
| **head -c 1024 file.txt**   | Pehle 1024 bytes dikhata hai                      | Binary file start check         |
| **tail file.txt**           | File ki aakhiri 10 lines dikhata hai              | Recent entries dekhna           |
| **tail -n 100 file.txt**    | Aakhiri 100 lines dikhata hai                     | More recent log entries         |
| **tail -f /var/log/syslog** | File ko real-time follow karta hai                | Live log monitoring - MOST USED |
| **tail -F file.log**        | File rotate hone ke baad bhi follow karta hai     | Production log tailing          |
| **wc -l file.txt**          | Line count nikalta hai                            | Log entries count karna         |
| **wc -c file.txt**          | Byte count nikalta hai                            | File size bytes mein            |
| **wc -w file.txt**          | Word count nikalta hai                            | Text analysis                   |

# **2\. Text Processing - grep, awk, sed, cut, sort, uniq**

Text processing Linux ka core strength hai. Logs parse karna, configs modify karna, output filter karna - ye sab daily ka kaam hai DevOps/SRE engineers ka.

## **2.1 grep - Pattern Search**

| **Command / Syntax**                | **Kya Karta Hai**                             | **Kyu Use Karte Hain**     |
| ----------------------------------- | --------------------------------------------- | -------------------------- |
| **grep 'error' app.log**            | File mein 'error' pattern dhundta hai         | Log errors dhundne ke liye |
| **grep -i 'ERROR' app.log**         | Case-insensitive search                       | Mixed case logs mein       |
| **grep -r 'password' /etc/**        | Recursively directory mein search             | Config files scan karna    |
| **grep -n 'failed' syslog**         | Match ke saath line number dikhata hai        | Exact line locate karna    |
| **grep -v 'INFO' app.log**          | Match nahi karne wali lines dikhata hai       | Noise filter karna         |
| **grep -c 'ERROR' app.log**         | Matching lines ka count dikhata hai           | Error frequency check      |
| **grep -l 'timeout' /var/log/\***   | Sirf file names jo match karte hain           | Files identify karna       |
| **grep -A 3 'ERROR' app.log**       | Match ke baad 3 lines bhi dikhata hai         | Context dekhne ke liye     |
| **grep -B 3 'ERROR' app.log**       | Match se pehle 3 lines dikhata hai            | Before-context dekhna      |
| **grep -C 3 'ERROR' app.log**       | Match ke aage-peeche 3 lines dikhata hai      | Full context analysis      |
| **grep -E 'error\|warn\|crit' log** | Extended regex: multiple patterns             | Multiple pattern match     |
| **grep -P '\\d{3}-\\d{4}'**         | Perl-compatible regex use karta hai           | Complex patterns ke liye   |
| **grep -w 'fail' log**              | Exact whole word match only                   | Partial match avoid karna  |
| **grep -o 'IP:\[0-9.\]\*' log**     | Sirf matched part print karta hai             | Data extraction            |
| **grep --color=auto 'err' log**     | Matches highlight karta hai (usually default) | Visual debugging           |
| **grep -m 10 'error' log**          | Maximum 10 matches pe rok jaata hai           | Quick sample dekhna        |
| **zgrep 'error' file.log.gz**       | Compressed .gz file mein grep karta hai       | Archived logs search       |

## **2.2 awk - Column & Field Processing**

| **Command / Syntax**                     | **Kya Karta Hai**                                | **Kyu Use Karte Hain** |
| ---------------------------------------- | ------------------------------------------------ | ---------------------- |
| **awk '{print \$1}' file**               | Pehla column (space-separated) print karta hai   | Field extraction       |
| **awk '{print \$1,\$3}' file**           | 1st aur 3rd column print karta hai               | Multiple fields        |
| **awk -F: '{print \$1}' /etc/passwd**    | Colon delimiter use karke user names nikalta hai | Custom delimiter       |
| **awk '{print NR, \$0}' file**           | Line number ke saath puri line print karta hai   | Line numbering         |
| **awk 'NR==5' file**                     | Sirf 5th line print karta hai                    | Specific line extract  |
| **awk 'NR>=5 && NR<=10' file**           | Lines 5 se 10 tak print karta hai                | Line range extract     |
| **awk '/ERROR/{print}' file**            | ERROR wali lines print karta hai                 | Pattern-based filter   |
| **awk '\$3 > 100' file**                 | 3rd field 100 se zyada wali lines                | Numeric filtering      |
| **awk '{sum+=\$1} END{print sum}' f**    | Column ka sum nikalta hai                        | Numeric aggregation    |
| **awk 'END{print NR}' file**             | Total line count nikalta hai                     | wc -l alternative      |
| **awk '{print \$NF}' file**              | Last field print karta hai                       | Last column extract    |
| **awk -F, '{print \$2}' csv**            | CSV ki 2nd column nikalta hai                    | CSV processing         |
| **awk '{print FILENAME, \$0}'**          | File name ke saath output print karta hai        | Multi-file processing  |
| **awk 'length(\$0)>80' file**            | 80 char se lambi lines filter karta hai          | Long line detection    |
| **awk '{gsub(/foo/,"bar"); print}'**     | foo ko bar se replace karke print karta hai      | Inline text replace    |
| **ps aux \| awk '{print \$2,\$3,\$11}'** | PID, CPU%, Command columns dikhata hai           | Process info extract   |

## **2.3 sed - Stream Editor**

| **Command / Syntax**              | **Kya Karta Hai**                                        | **Kyu Use Karte Hain** |
| --------------------------------- | -------------------------------------------------------- | ---------------------- |
| **sed 's/old/new/' file**         | Pehli occurrence replace karta hai per line              | Text substitution      |
| **sed 's/old/new/g' file**        | Saari occurrences replace karta hai                      | Global replace         |
| **sed -i 's/old/new/g' file**     | File in-place edit karta hai (original change)           | Direct file editing    |
| **sed -i.bak 's/x/y/g' file**     | Backup banake in-place edit karta hai                    | Safe in-place edit     |
| **sed -n '5,10p' file**           | Lines 5 se 10 tak print karta hai                        | Line range extract     |
| **sed -n '/ERROR/p' file**        | Sirf ERROR wali lines print karta hai                    | Pattern filter         |
| **sed '/^#/d' file**              | Hash se shuru hone wali (comment) lines delete karta hai | Comment removal        |
| **sed '/^\$/d' file**             | Blank lines delete karta hai                             | Clean up empty lines   |
| **sed '5d' file**                 | 5th line delete karta hai                                | Specific line remove   |
| **sed 's/^/ /' file**             | Har line ke aage 4 spaces add karta hai                  | Indentation add karna  |
| **sed 's/ \*\$//' file**          | Trailing whitespace remove karta hai                     | Whitespace cleanup     |
| **sed 's/\\t/,/g' file**          | Tabs ko commas se replace karta hai                      | TSV to CSV convert     |
| **sed -n '1p' file**              | Sirf pehli line print karta hai                          | First line extract     |
| **sed '\$d' file**                | Last line delete karta hai                               | Remove last entry      |
| **sed '1i\\New First Line' file** | Pehli line ke upar naya content insert karta hai         | Header add karna       |
| **sed '\$ a\\Last Line' file**    | File ke end mein line append karta hai                   | Footer add karna       |

## **2.4 cut, sort, uniq, tr, paste**

| **Command / Syntax**                 | **Kya Karta Hai**                                      | **Kyu Use Karte Hain**  |
| ------------------------------------ | ------------------------------------------------------ | ----------------------- |
| **cut -d: -f1 /etc/passwd**          | Colon separator se 1st field cut karta hai             | Field extraction        |
| **cut -d, -f2,4 file.csv**           | CSV se 2nd aur 4th columns nikalta hai                 | CSV column select       |
| **cut -c1-10 file**                  | Character 1 se 10 tak cut karta hai                    | Fixed-width fields      |
| **sort file.txt**                    | Alphabetically sort karta hai                          | Data sorting            |
| **sort -n numbers.txt**              | Numerically sort karta hai                             | Numeric sort            |
| **sort -rn file**                    | Reverse numeric sort (largest first)                   | Top N dekhne ke liye    |
| **sort -k2 file**                    | 2nd field se sort karta hai                            | Column-specific sort    |
| **sort -t: -k3 -n /etc/passwd**      | Colon-sep, 3rd field numerically sort                  | UID sort                |
| **sort -u file**                     | Sort karta hai aur duplicates remove karta hai         | Unique sorted output    |
| **uniq file**                        | Consecutive duplicate lines remove karta hai           | Dedup (sort pehle karo) |
| **uniq -c file**                     | Count ke saath unique lines dikhata hai                | Frequency count         |
| **uniq -d file**                     | Sirf duplicate lines dikhata hai                       | Find duplicates         |
| **sort file \| uniq -c \| sort -rn** | Top frequent lines nikalta hai                         | Log frequency analysis  |
| **tr 'a-z' 'A-Z'**                   | Lowercase ko uppercase mein convert karta hai          | Case conversion         |
| **tr -d '\\r'**                      | Carriage return (Windows) chars delete karta hai       | Windows to Unix convert |
| **tr -s ' '**                        | Multiple spaces ko single space mein squeeze karta hai | Whitespace normalize    |
| **paste file1 file2**                | Two files ko side-by-side join karta hai               | Column merging          |
| **paste -d, f1 f2**                  | Comma se join karta hai (CSV banana)                   | CSV creation            |

# **3\. File Permissions, Ownership & Special Bits**

Linux mein security ka foundation hai file permissions. Production servers pe wrong permissions = security breach ya application failure. Ye samajhna bahut zaroori hai.

## **3.1 Permission Format Samjho**

| ls -la /etc/passwd                                           |
| ------------------------------------------------------------ |
| \-rw-r--r-- 1 root root 2867 Jan 15 10:23 /etc/passwd        |
|                                                              |
| Format: \[type\]\[user-perms\]\[group-perms\]\[other-perms\] |
| \- rw- r-- r--                                               |
|                                                              |
| File Types: - = regular file d = directory l = symlink       |
| b = block device c = char device p = pipe                    |
|                                                              |
| Permissions: r = read (4) w = write (2) x = execute (1)      |
|                                                              |
| Octal Examples:                                              |
| 777 = rwxrwxrwx (everyone all access - BAD for prod!)        |
| 755 = rwxr-xr-x (owner all, others read+exec - executables)  |
| 644 = rw-r--r-- (owner r/w, others read - config files)      |
| 600 = rw------- (owner only - SSH keys, secrets)             |
| 700 = rwx------ (owner only execute - private scripts)       |
| 640 = rw-r----- (owner r/w, group read - app configs)        |

## **3.2 chmod - Change Permissions**

| **Command / Syntax**           | **Kya Karta Hai**                            | **Kyu Use Karte Hain**     |
| ------------------------------ | -------------------------------------------- | -------------------------- |
| **chmod 755 script.sh**        | rwxr-xr-x set karta hai - executable script  | Script execute permissions |
| **chmod 644 config.conf**      | rw-r--r-- set karta hai - config file        | Config file protection     |
| **chmod 600 ~/.ssh/id_rsa**    | Private key - sirf owner read/write          | SSH key security (MUST!)   |
| **chmod 700 ~/.ssh**           | SSH dir - sirf owner access                  | SSH dir protection         |
| **chmod +x deploy.sh**         | Execute bit add karta hai (all users)        | Script executable banana   |
| **chmod -x script.sh**         | Execute bit remove karta hai                 | Execution disable karna    |
| **chmod u+x,g-w file**         | User ko x add, group se w remove             | Fine-grained permission    |
| **chmod o-rwx secret.conf**    | Others ke saare permissions remove karta hai | Restrict public access     |
| **chmod a=r file**             | Sabko sirf read permission deta hai          | Read-only for everyone     |
| **chmod -R 755 /var/www/html** | Recursively sab files pe apply karta hai     | Web server permissions     |
| **chmod g+s /shared/dir**      | SetGID - naye files group inherit karte hain | Shared directory setup     |
| **chmod +t /tmp**              | Sticky bit - sirf owner file delete kar sake | /tmp protection            |
| **chmod 4755 /usr/bin/passwd** | SetUID - root privileges se run karna        | Special privilege binary   |

## **3.3 chown & chgrp - Ownership Change**

| **Command / Syntax**                    | **Kya Karta Hai**                            | **Kyu Use Karte Hain** |
| --------------------------------------- | -------------------------------------------- | ---------------------- |
| **chown john file.txt**                 | File owner john ko set karta hai             | File ownership change  |
| **chown john:developers file.txt**      | Owner aur group dono set karta hai           | Owner+group set karna  |
| **chown -R www-data:www-data /var/www** | Web files recursively nginx user ko deta hai | Web server setup       |
| **chown root:root /etc/sudoers**        | Critical config files root ko deta hai       | Security hardening     |
| **chgrp docker /var/run/docker.sock**   | Docker socket ka group change karta hai      | Docker permissions     |
| **chown --reference=ref.txt f**         | ref.txt ki ownership copy karta hai          | Matching ownership set |
| **ls -la /etc/shadow**                  | Shadow file permissions verify karta hai     | Security audit         |

## **3.4 sudo & su - Privilege Escalation**

| **Command / Syntax**      | **Kya Karta Hai**                               | **Kyu Use Karte Hain**    |
| ------------------------- | ----------------------------------------------- | ------------------------- |
| **sudo command**          | Root privileges se command run karta hai        | Admin tasks ke liye       |
| **sudo -i**               | Root shell open karta hai (login shell)         | Multiple root commands    |
| **sudo -u john command**  | John user ki taraf se command run karta hai     | Other user se run karna   |
| **sudo -l**               | Current user ke sudo permissions list karta hai | Permission check          |
| **sudo !!**               | Previous command sudo se rerun karta hai        | Forgot sudo? Quick fix    |
| **su -**                  | Root user mein switch karta hai (login shell)   | Full root environment     |
| **su - john**             | John user mein switch karta hai                 | User switch karna         |
| **visudo**                | sudoers file safely edit karta hai              | NEVER direct edit sudoers |
| **sudo cat /etc/sudoers** | Sudoers file read karta hai                     | Permissions audit         |

# **4\. Process Management**

Production mein processes monitor karna aur manage karna SRE/DevOps ka daily kaam hai. CPU spike kyo aaya? Memory leak kaun kar raha hai? Zombie processes? Sab yahan.

## **4.1 Process Viewing**

| **Command / Syntax**                     | **Kya Karta Hai**                           | **Kyu Use Karte Hain**  |
| ---------------------------------------- | ------------------------------------------- | ----------------------- |
| **ps**                                   | Current terminal ke processes dikhata hai   | Basic process view      |
| **ps aux**                               | ALL users ke ALL processes dikhata hai      | Full process list       |
| **ps aux \| grep nginx**                 | Nginx process dhundta hai                   | Specific process find   |
| **ps -ef**                               | Full format - PPID bhi dikhata hai          | Parent process dekhna   |
| **ps -e --forest**                       | Process tree (parent-child) dikhata hai     | Process hierarchy       |
| **ps -u www-data**                       | Specific user ke processes                  | User-specific processes |
| **ps aux --sort=-%cpu**                  | CPU usage se sort karta hai (highest first) | CPU hog find karna      |
| **ps aux --sort=-%mem**                  | Memory usage se sort karta hai              | Memory hog find karna   |
| **ps -p 1234 -o pid,ppid,cmd,%cpu,%mem** | Specific PID ki details                     | Single process details  |
| **pgrep nginx**                          | Process name se PID nikalta hai             | PID dhundna             |
| **pgrep -u www-data**                    | User ke saare PIDs nikalta hai              | User PIDs find          |
| **pidof nginx**                          | nginx ke saare PIDs dikhata hai             | All instances PID       |

## **4.2 top & htop - Real-time Monitoring**

| **Command / Syntax** | **Kya Karta Hai**                       | **Kyu Use Karte Hain**           |
| -------------------- | --------------------------------------- | -------------------------------- |
| **top**              | Real-time process monitor (CPU/MEM/PID) | System health check              |
| **top -u www-data**  | Specific user ke processes top mein     | User-specific monitoring         |
| **top -p 1234**      | Sirf specific PID monitor karta hai     | Single process watch             |
| **top -b -n 1**      | Batch mode - scripting ke liye output   | Automated monitoring             |
| **htop**             | Interactive, colorful top (better UI)   | Daily monitoring - install first |
| **htop -u john**     | John user ke processes htop mein        | User filter in htop              |
| **atop**             | Advanced process+disk+network monitor   | Detailed analysis                |
| **glances**          | All-in-one system overview              | Quick system snapshot            |

**TOP KEYS:** P=CPU sort, M=Memory sort, k=kill, r=renice, q=quit, 1=per-CPU, H=threads toggle, F=fields select

## **4.3 Process Signals & Kill**

| **Command / Syntax**      | **Kya Karta Hai**                                    | **Kyu Use Karte Hain**         |
| ------------------------- | ---------------------------------------------------- | ------------------------------ |
| **kill 1234**             | PID 1234 ko SIGTERM (15) bhejta hai - graceful stop  | Process gracefully stop karna  |
| **kill -9 1234**          | SIGKILL - force kill (process handle nahi kar sakta) | Hung process force kill        |
| **kill -HUP 1234**        | SIGHUP - config reload karta hai (nginx, etc.)       | Service reload without restart |
| **kill -0 1234**          | PID exist karta hai ya nahi check karta hai          | Process existence check        |
| **killall nginx**         | Name se saare matching processes kill karta hai      | All instances kill             |
| **pkill -f 'python app'** | Command pattern se process kill karta hai            | Pattern-based kill             |
| **pkill -u john**         | John user ke saare processes kill karta hai          | User session cleanup           |
| **kill -l**               | Saare signal numbers aur names list karta hai        | Available signals dekhna       |

## **4.4 Background Jobs & Job Control**

| **Command / Syntax** | **Kya Karta Hai**                                     | **Kyu Use Karte Hain**    |
| -------------------- | ----------------------------------------------------- | ------------------------- |
| **command &**        | Background mein run karta hai                         | Long task background mein |
| **jobs**             | Current shell ke background jobs list karta hai       | Running jobs dekhna       |
| **fg**               | Most recent job foreground mein laata hai             | Background se foreground  |
| **fg %2**            | Job number 2 foreground mein laata hai                | Specific job foreground   |
| **bg**               | Stopped job background mein resume karta hai          | Job resume in background  |
| **Ctrl+\\**          | Running process ko SIGQUIT bhejta hai (core dump)     | Force quit with core dump |
| **Ctrl+S / Ctrl+Q**  | Terminal output pause / resume karta hai              | Terminal flow control     |
| **nohup cmd &**      | Terminal close hone ke baad bhi process chalti rahe   | Long-running tasks        |
| **disown %1**        | Job ko shell se detach karta hai                      | nohup alternative         |
| **wait**             | Saare background jobs complete hone ka wait karta hai | Scripting synchronization |
| **wait 1234**        | Specific PID complete hone ka wait karta hai          | Single job wait           |

## **4.5 Process Priority - nice & renice**

| **Command / Syntax**     | **Kya Karta Hai**                                    | **Kyu Use Karte Hain**            |
| ------------------------ | ---------------------------------------------------- | --------------------------------- |
| **nice -n 10 command**   | Low priority (10) ke saath start karta hai           | Resource-intensive tasks throttle |
| **nice -n -5 command**   | Higher priority (-5) ke saath start karta hai (sudo) | Critical task prioritize          |
| **renice -n 5 -p 1234**  | Running process 1234 ki priority change karta hai    | Live priority adjustment          |
| **renice -n 10 -u john** | John ke saare processes ki priority change karta hai | User-level throttling             |

**NICE VALUES:** Range: -20 (highest priority) to +19 (lowest priority). Default = 0. Negative values need sudo.

# **5\. Networking Commands**

Network troubleshooting, connectivity check, port monitoring, firewall management - ye sab DevOps/SRE ka daily kaam hai. Yahan sab essential commands hain.

## **5.1 Network Interface & IP**

| **Command / Syntax**                        | **Kya Karta Hai**                                  | **Kyu Use Karte Hain**     |
| ------------------------------------------- | -------------------------------------------------- | -------------------------- |
| **ip addr**                                 | Network interfaces aur IP addresses dikhata hai    | IP address check karna     |
| **ip addr show eth0**                       | Specific interface ki details dikhata hai          | Interface specific info    |
| **ip link**                                 | Network interfaces ka status dikhata hai (UP/DOWN) | Interface status check     |
| **ip link set eth0 up**                     | Interface eth0 ko enable karta hai                 | Interface UP karna         |
| **ip link set eth0 down**                   | Interface eth0 ko disable karta hai                | Interface DOWN karna       |
| **ip route**                                | Routing table dikhata hai                          | Routes dekhna              |
| **ip route add 10.0.0.0/8 via 192.168.1.1** | Static route add karta hai                         | Custom routing             |
| **ip route del default**                    | Default gateway remove karta hai                   | Route management           |
| **ifconfig**                                | Legacy: network interface info (deprecated)        | Old systems mein           |
| **ifconfig eth0**                           | Specific interface info dikhata hai                | Legacy interface check     |
| **hostname**                                | Current hostname dikhata hai                       | Server identity check      |
| **hostname -I**                             | Saare IP addresses dikhata hai                     | All IPs list karna         |
| **hostnamectl**                             | Systemd hostname management tool                   | Modern hostname management |
| **hostnamectl set-hostname srv**            | Hostname permanently change karta hai              | Server rename karna        |

## **5.2 Connectivity Testing**

| **Command / Syntax**                           | **Kya Karta Hai**                                | **Kyu Use Karte Hain**     |
| ---------------------------------------------- | ------------------------------------------------ | -------------------------- |
| **ping google.com**                            | ICMP packets bhejke connectivity test karta hai  | Basic connectivity check   |
| **ping -c 4 8.8.8.8**                          | Exactly 4 packets bhejta hai                     | Limited ping test          |
| **ping -i 0.5 -s 1000 host**                   | Interval aur packet size set karke ping          | Custom ping test           |
| **traceroute google.com**                      | Packets ka route trace karta hai                 | Network path debugging     |
| **traceroute -n google.com**                   | DNS resolve nahi karta (faster)                  | Quick traceroute           |
| **mtr google.com**                             | Continuous ping+traceroute combined              | Network quality monitoring |
| **mtr --report google.com**                    | Report mode - one-time output                    | Network path report        |
| **curl -I <https://google.com>**               | HTTP headers only check karta hai                | HTTP response check        |
| **curl -o /dev/null -s -w '%{http_code}' URL** | HTTP status code check karta hai                 | Health check scripting     |
| **curl -v <https://api.com>**                  | Verbose - full request/response details          | API debugging              |
| **curl -L URL**                                | Redirects follow karta hai                       | Redirect chain check       |
| **wget URL**                                   | File download karta hai                          | File download              |
| **wget -q --spider URL**                       | URL accessible hai check karta hai (no download) | Link check                 |

## **5.3 DNS Tools**

| **Command / Syntax**         | **Kya Karta Hai**                      | **Kyu Use Karte Hain**    |
| ---------------------------- | -------------------------------------- | ------------------------- |
| **nslookup google.com**      | DNS lookup karta hai                   | DNS resolution check      |
| **nslookup -type=MX domain** | MX (mail) records nikalta hai          | Mail server DNS check     |
| **dig google.com**           | Detailed DNS query karta hai           | DNS debugging - preferred |
| **dig google.com A**         | A (IPv4) records query karta hai       | IPv4 address lookup       |
| **dig google.com AAAA**      | AAAA (IPv6) records query karta hai    | IPv6 address lookup       |
| **dig google.com MX**        | Mail exchange records                  | Email routing check       |
| **dig google.com NS**        | Nameserver records                     | Authoritative NS find     |
| **dig @8.8.8.8 google.com**  | Specific DNS server se query karta hai | Custom DNS server test    |
| **dig +short google.com**    | Sirf IP address print karta hai        | Quick IP lookup           |
| **dig -x 8.8.8.8**           | Reverse DNS lookup (IP se hostname)    | PTR record check          |
| **host google.com**          | Simple DNS lookup                      | Quick hostname resolution |
| **cat /etc/resolv.conf**     | Configured DNS servers dikhata hai     | DNS config check          |
| **cat /etc/hosts**           | Local hostname-IP mappings dikhata hai | Local DNS override check  |

## **5.4 Port & Socket Monitoring**

| **Command / Syntax**      | **Kya Karta Hai**                            | **Kyu Use Karte Hain**       |
| ------------------------- | -------------------------------------------- | ---------------------------- |
| **ss -tuln**              | TCP+UDP listening ports dikhata hai          | Open ports check - PREFERRED |
| **ss -tulnp**             | Process name bhi dikhata hai                 | Which process owns port      |
| **ss -ta**                | All TCP connections (established+listening)  | All TCP connections          |
| **ss -s**                 | Socket statistics summary                    | Quick socket overview        |
| **ss -p \| grep firefox** | Firefox ki sockets dikhata hai               | App-specific sockets         |
| **netstat -tuln**         | Legacy: listening ports (deprecated, use ss) | Old systems compatibility    |
| **netstat -anp**          | All connections with PID                     | Legacy port check            |
| **lsof -i :80**           | Port 80 use karne wale processes dikhata hai | Port owner find karna        |
| **lsof -i :8080-8090**    | Port range use karne wale processes          | Port range check             |
| **lsof -i tcp**           | Saare TCP connections list karta hai         | TCP connection audit         |
| **lsof -u john**          | John user ke open files/sockets              | User connection audit        |
| **nc -zv host 80**        | Port 80 open hai check karta hai             | Remote port check            |
| **nc -zv host 8080-8090** | Port range check karta hai                   | Service availability         |
| **nc -l 8888**            | Port 8888 pe listen karta hai (server mode)  | Quick TCP server test        |

## **5.5 Firewall - iptables & firewalld**

| **Command / Syntax**                              | **Kya Karta Hai**                            | **Kyu Use Karte Hain** |
| ------------------------------------------------- | -------------------------------------------- | ---------------------- |
| **iptables -L -n -v**                             | Firewall rules list karta hai                | Current rules check    |
| **iptables -A INPUT -p tcp --dport 22 -j ACCEPT** | SSH (port 22) allow karta hai                | SSH access allow       |
| **iptables -A INPUT -p tcp --dport 80 -j ACCEPT** | HTTP allow karta hai                         | Web traffic allow      |
| **iptables -A INPUT -s 192.168.1.0/24 -j ACCEPT** | Network subnet allow karta hai               | Network-level allow    |
| **iptables -A INPUT -j DROP**                     | Baaki sab INPUT traffic drop karta hai       | Default deny rule      |
| **iptables -D INPUT 3**                           | 3rd rule delete karta hai                    | Rule remove karna      |
| **iptables -F**                                   | Saari rules flush/clear karta hai (careful!) | Rules reset karna      |
| **iptables-save > rules.txt**                     | Current rules save karta hai                 | Rules backup           |
| **iptables-restore < rules.txt**                  | Rules restore karta hai                      | Rules restore          |
| **firewall-cmd --list-all**                       | firewalld: current zone rules dikhata hai    | CentOS/RHEL firewall   |
| **firewall-cmd --add-port=8080/tcp --permanent**  | Port 8080 permanently allow karta hai        | Add port to firewall   |
| **firewall-cmd --reload**                         | firewalld reload karta hai                   | Apply firewall changes |
| **ufw status**                                    | Ubuntu firewall status dikhata hai           | UFW status check       |
| **ufw allow 443/tcp**                             | HTTPS allow karta hai                        | UFW port allow         |
| **ufw deny from 1.2.3.4**                         | Specific IP block karta hai                  | IP blocking            |

# **6\. Disk & Storage Management**

Disk space khatam hona production outage ka ek common reason hai. Disk monitoring, mounting, partitioning - ye sab zaroor aana chahiye ek DevOps/SRE engineer ko.

## **6.1 Disk Usage & Space**

| **Command / Syntax**                     | **Kya Karta Hai**                                  | **Kyu Use Karte Hain**   |
| ---------------------------------------- | -------------------------------------------------- | ------------------------ |
| **df -h**                                | All mounted filesystems ki space usage dikhata hai | Disk space check - DAILY |
| **df -hT**                               | Filesystem type bhi dikhata hai                    | FS type check            |
| **df -i**                                | Inode usage dikhata hai                            | Inode exhaustion check   |
| **df -h /var**                           | Specific partition ki space check karta hai        | Single partition check   |
| **du -sh /var/log**                      | Directory ka total size dikhata hai                | Folder size check        |
| **du -sh /\***                           | Root ke har subfolder ka size                      | Identify space hogs      |
| **du -h --max-depth=2 /var**             | 2 levels deep size breakdown                       | Detailed space analysis  |
| **du -ah /etc/ \| sort -rh \| head -20** | Top 20 largest files/dirs nikalta hai              | Find largest files       |
| **ncdu /**                               | Interactive disk usage (install: apt install ncdu) | Visual disk explorer     |
| **lsblk**                                | Block devices tree format mein dikhata hai         | Disk/partition layout    |
| **lsblk -f**                             | Filesystem type aur UUID bhi dikhata hai           | FS type verification     |
| **fdisk -l**                             | Disk partitions list karta hai (sudo)              | Partition table view     |
| **blkid**                                | Block devices ke UUID aur filesystem type          | Device identification    |

## **6.2 Mounting & Unmounting**

| **Command / Syntax**             | **Kya Karta Hai**                            | **Kyu Use Karte Hain** |
| -------------------------------- | -------------------------------------------- | ---------------------- |
| **mount**                        | Currently mounted filesystems dikhata hai    | Mounts check karna     |
| **mount /dev/sdb1 /mnt/data**    | Disk ko /mnt/data pe mount karta hai         | Manual disk mount      |
| **mount -t ext4 /dev/sdb1 /mnt** | Specific filesystem type ke saath mount      | FS type specify karna  |
| **mount -o ro /dev/sdb1 /mnt**   | Read-only mount karta hai                    | Read-only access       |
| **mount -o remount,rw /**        | Root FS ko r/w remount karta hai             | Remount with options   |
| **umount /mnt/data**             | Filesystem unmount karta hai                 | Safe disk remove       |
| **umount -l /mnt/data**          | Lazy unmount - busy hone pe bhi              | Forced unmount         |
| **cat /etc/fstab**               | Boot pe auto-mount configuration dikhata hai | fstab config check     |
| **mount -a**                     | fstab ke saare entries mount karta hai       | fstab apply karna      |

## **6.3 Disk Operations**

| **Command / Syntax**                      | **Kya Karta Hai**                       | **Kyu Use Karte Hain**   |
| ----------------------------------------- | --------------------------------------- | ------------------------ |
| **dd if=/dev/zero of=file bs=1G count=1** | 1GB test file create karta hai          | Disk write speed test    |
| **dd if=/dev/sda of=/dev/sdb bs=64K**     | Disk clone karta hai                    | Disk-to-disk copy        |
| **sync**                                  | Disk buffers flush karta hai            | Safe unmount ke pehle    |
| **fsck /dev/sdb1**                        | Filesystem check aur repair (unmounted) | Disk health check        |
| **e2fsck -f /dev/sdb1**                   | ext4 filesystem force check             | ext4 specific check      |
| **mkfs.ext4 /dev/sdb1**                   | ext4 filesystem banata hai              | New disk format          |
| **mkfs.xfs /dev/sdb1**                    | XFS filesystem banata hai               | XFS format (RHEL/CentOS) |
| **tune2fs -l /dev/sda1**                  | ext filesystem details dikhata hai      | FS metadata check        |
| **resize2fs /dev/sda1**                   | ext2/3/4 FS resize karta hai            | Partition resize ke baad |
| **parted /dev/sdb**                       | Partition management tool               | Disk partitioning        |
| **fdisk /dev/sdb**                        | Interactive partition editor            | MBR partition creation   |
| **gdisk /dev/sdb**                        | GPT partition editor                    | Modern partition create  |

## **6.4 Logical Volume Management (LVM)**

| **Command / Syntax**                  | **Kya Karta Hai**                     | **Kyu Use Karte Hain**    |
| ------------------------------------- | ------------------------------------- | ------------------------- |
| **pvdisplay**                         | Physical volumes (PV) dikhata hai     | LVM PV info               |
| **vgdisplay**                         | Volume groups (VG) dikhata hai        | LVM VG info               |
| **lvdisplay**                         | Logical volumes (LV) dikhata hai      | LVM LV info               |
| **pvcreate /dev/sdb**                 | Disk ko PV banata hai                 | LVM setup step 1          |
| **vgcreate datavg /dev/sdb**          | Volume group create karta hai         | LVM setup step 2          |
| **lvcreate -L 20G -n data datavg**    | 20GB logical volume create karta hai  | LVM setup step 3          |
| **lvextend -L +10G /dev/datavg/data** | LV ko 10GB extend karta hai           | LV expand karna           |
| **resize2fs /dev/datavg/data**        | LV extend ke baad FS resize karta hai | FS expand after LV extend |
| **lvremove /dev/datavg/data**         | Logical volume delete karta hai       | LV cleanup                |
| **vgs**                               | Volume groups quick summary           | Quick VG check            |
| **lvs**                               | Logical volumes quick summary         | Quick LV check            |

# **7\. System Monitoring & Performance**

Production systems mein performance issues diagnose karna - CPU, memory, disk I/O, network - ye sab SRE ka core skill hai.

## **7.1 CPU & Memory Monitoring**

| **Command / Syntax** | **Kya Karta Hai**                              | **Kyu Use Karte Hain**     |
| -------------------- | ---------------------------------------------- | -------------------------- |
| **free -h**          | RAM aur swap usage dikhata hai                 | Memory status check        |
| **free -h -s 2**     | Har 2 seconds pe refresh karta hai             | Continuous memory monitor  |
| **vmstat 1 5**       | CPU/memory/io stats har 1 sec, 5 times         | Performance overview       |
| **vmstat -s**        | Memory stats summary dikhata hai               | Memory detailed stats      |
| **mpstat -P ALL 1**  | Per-CPU statistics dikhata hai                 | Multi-core CPU monitoring  |
| **mpstat 1 5**       | Overall CPU stats har 1 sec, 5 times           | CPU utilization check      |
| **sar -u 1 5**       | CPU utilization (System Activity Report)       | Historical CPU analysis    |
| **sar -r 1 5**       | Memory utilization report                      | Historical memory analysis |
| **sar -b 1 5**       | I/O stats report                               | Historical I/O analysis    |
| **uptime**           | Load average aur uptime dikhata hai            | Quick system health        |
| **w**                | Who is logged in + system load dikhata hai     | User + load check          |
| **iostat**           | CPU aur disk I/O statistics dikhata hai        | I/O bottleneck find        |
| **iostat -x 1 5**    | Extended I/O stats har 1 sec                   | Detailed disk I/O          |
| **dstat**            | All stats combined (install separately)        | Comprehensive monitoring   |
| **iotop**            | Per-process disk I/O usage (like top for disk) | Disk I/O hog find          |
| **iotop -o**         | Sirf active I/O processes dikhata hai          | Active I/O monitoring      |

## **7.2 System Information**

| **Command / Syntax**       | **Kya Karta Hai**                            | **Kyu Use Karte Hain**  |
| -------------------------- | -------------------------------------------- | ----------------------- |
| **uname -a**               | Kernel version aur architecture dikhata hai  | Kernel info check       |
| **uname -r**               | Sirf kernel version                          | Kernel version check    |
| **cat /etc/os-release**    | OS distribution aur version dikhata hai      | Linux distro identify   |
| **lsb_release -a**         | Distro info (Ubuntu/Debian systems pe)       | Ubuntu version check    |
| **cat /proc/cpuinfo**      | CPU details (cores, model, speed)            | CPU hardware info       |
| **nproc**                  | Available CPU cores ki count                 | CPU count for scripting |
| **lscpu**                  | CPU architecture detailed info               | Complete CPU info       |
| **cat /proc/meminfo**      | Detailed memory information                  | Memory details          |
| **dmidecode -t system**    | Hardware manufacturer info (sudo needed)     | Hardware vendor info    |
| **lshw -short**            | Hardware summary (sudo needed)               | Hardware inventory      |
| **lspci**                  | PCI devices list karta hai                   | Hardware devices check  |
| **lsusb**                  | USB devices list karta hai                   | USB device check        |
| **dmesg**                  | Kernel ring buffer messages                  | Kernel/hardware errors  |
| **dmesg -T**               | Human-readable timestamps ke saath dmesg     | Timestamped kernel logs |
| **dmesg \| grep -i error** | Kernel error messages filter karta hai       | Hardware error check    |
| **last**                   | Login history dikhata hai                    | User login audit        |
| **lastb**                  | Failed login attempts dikhata hai            | Security breach check   |
| **who**                    | Currently logged in users dikhata hai        | Active sessions check   |
| **id**                     | Current user ki UID, GID, groups dikhata hai | Identity check          |

## **7.3 Log Management**

| **Command / Syntax**                                     | **Kya Karta Hai**                      | **Kyu Use Karte Hain**  |
| -------------------------------------------------------- | -------------------------------------- | ----------------------- |
| **journalctl**                                           | Systemd journal saare logs dikhata hai | System logs access      |
| **journalctl -f**                                        | Real-time logs follow karta hai        | Live log monitoring     |
| **journalctl -u nginx**                                  | nginx service ke specific logs         | Service-specific logs   |
| **journalctl -u nginx --since today**                    | Aaj ke nginx logs                      | Today's service logs    |
| **journalctl -p err**                                    | Sirf error level logs dikhata hai      | Error logs filter       |
| **journalctl --since '1 hour ago'**                      | Last 1 hour ke logs                    | Recent logs check       |
| **journalctl --since '2024-01-15' --until '2024-01-16'** | Date range logs                        | Specific time logs      |
| **journalctl -n 100**                                    | Last 100 log entries                   | Recent log entries      |
| **journalctl --disk-usage**                              | Journal disk usage dikhata hai         | Log space check         |
| **journalctl --vacuum-size=1G**                          | Journal ko 1GB tak limit karta hai     | Log cleanup             |
| **tail -f /var/log/kern.log**                            | Kernel logs real-time follow karta hai | Kernel event monitoring |
| **tail -f /var/log/auth.log**                            | Authentication logs monitor karta hai  | Security monitoring     |
| **tail -f /var/log/nginx/access.log**                    | Nginx access logs real-time            | Web traffic monitoring  |
| **grep -i error /var/log/syslog \| tail -50**            | Recent errors check karta hai          | Quick error check       |
| **logrotate -f /etc/logrotate.conf**                     | Log rotation force karta hai           | Manual log rotate       |

# **8\. Systemd & Service Management**

Modern Linux systems mein systemd hi init system hai. Services start/stop/enable karna, service create karna - ye sab daily kaam hai.

## **8.1 systemctl - Service Control**

| **Command / Syntax**                    | **Kya Karta Hai**                                    | **Kyu Use Karte Hain**      |
| --------------------------------------- | ---------------------------------------------------- | --------------------------- |
| **systemctl status nginx**              | Service ka current status dikhata hai                | Service health check        |
| **systemctl start nginx**               | Service start karta hai                              | Service start karna         |
| **systemctl stop nginx**                | Service gracefully stop karta hai                    | Service stop karna          |
| **systemctl restart nginx**             | Service stop karke start karta hai                   | Service restart             |
| **systemctl reload nginx**              | Config reload (restart nahi)                         | Zero-downtime config update |
| **systemctl enable nginx**              | Boot pe auto-start enable karta hai                  | Service persist on reboot   |
| **systemctl disable nginx**             | Boot pe auto-start disable karta hai                 | Service remove from boot    |
| **systemctl enable --now nginx**        | Enable aur turant start karta hai                    | Enable+start together       |
| **systemctl is-active nginx**           | Service active hai ya nahi (returns active/inactive) | Script mein status check    |
| **systemctl is-enabled nginx**          | Service boot pe enabled hai ya nahi                  | Boot status check           |
| **systemctl list-units --type=service** | Saari services list karta hai                        | All services overview       |
| **systemctl list-units --failed**       | Failed services list karta hai                       | Failed service identify     |
| **systemctl daemon-reload**             | Unit files reload karta hai (new service ke baad)    | After editing unit files    |
| **systemctl mask nginx**                | Service ko completely disable karta hai              | Prevent service start       |
| **systemctl unmask nginx**              | Masked service ko restore karta hai                  | Re-enable masked service    |
| **systemctl poweroff**                  | System shutdown karta hai                            | Proper shutdown             |
| **systemctl reboot**                    | System reboot karta hai                              | System restart              |
| **systemctl suspend**                   | System suspend karta hai                             | Power management            |

## **8.2 Custom Systemd Service Banana**

| \# Step 1: Service unit file create karo                    |
| ----------------------------------------------------------- |
| sudo nano /etc/systemd/system/myapp.service                 |
|                                                             |
| \[Unit\]                                                    |
| Description=My Application Service                          |
| After=network.target # Network ready hone ke baad start ho  |
| Requires=network.target                                     |
|                                                             |
| \[Service\]                                                 |
| Type=simple                                                 |
| User=www-data                                               |
| WorkingDirectory=/opt/myapp                                 |
| ExecStart=/usr/bin/python3 /opt/myapp/app.py                |
| ExecReload=/bin/kill -HUP \$MAINPID                         |
| Restart=always # Crash pe auto-restart                      |
| RestartSec=5 # 5 seconds baad restart                       |
| StandardOutput=journal # Logs systemd journal mein          |
| StandardError=journal                                       |
| EnvironmentFile=/etc/myapp.env # Environment variables file |
|                                                             |
| \[Install\]                                                 |
| WantedBy=multi-user.target                                  |
|                                                             |
| \# Step 2: Enable aur start karo                            |
| sudo systemctl daemon-reload                                |
| sudo systemctl enable --now myapp                           |

## **8.3 systemd Timers (Cron Alternative)**

| **Command / Syntax**                              | **Kya Karta Hai**                  | **Kyu Use Karte Hain** |
| ------------------------------------------------- | ---------------------------------- | ---------------------- |
| **systemctl list-timers**                         | Saare active timers list karta hai | Scheduled tasks dekhna |
| **systemctl list-timers --all**                   | Inactive timers bhi dikhata hai    | All timers overview    |
| **systemctl status systemd-tmpfiles-clean.timer** | Specific timer status              | Timer health check     |

# **9\. Cron & Task Scheduling**

Automated tasks schedule karna - backups, log cleanup, health checks, reports - ye sab cron se hota hai. SRE engineers ko cron syntax aur management aana chahiye.

## **9.1 Cron Syntax**

| \# Cron format: MIN HOUR DAY MONTH WEEKDAY COMMAND          |
| ----------------------------------------------------------- |
| \# \* \* \* \* \*                                           |
|                                                             |
| \# Examples:                                                |
| \*/5 \* \* \* \* /script.sh # Har 5 minutes                 |
| 0 \* \* \* \* /script.sh # Har ghante mein (top of hour)    |
| 0 2 \* \* \* /backup.sh # Roz raat 2 baje                   |
| 0 2 \* \* 0 /weekly.sh # Har Sunday 2 baje                  |
| 0 2 1 \* \* /monthly.sh # Har mahine ki 1 tarikh 2 baje     |
| 0 9-18 \* \* 1-5 /work.sh # Weekdays 9am-6pm har ghante     |
| @reboot /startup.sh # Boot pe ek baar                       |
| @daily /daily.sh # Roz midnight (= 0 0 \* \* \*)            |
| @weekly /weekly.sh # Har sunday midnight                    |
| @monthly /monthly.sh # Har mahine 1 tarikh                  |
|                                                             |
| \# Wildcards:                                               |
| \* = every , = list (1,3,5) - = range (1-5) / = step (\*/5) |

## **9.2 Crontab Commands**

| **Command / Syntax**          | **Kya Karta Hai**                                          | **Kyu Use Karte Hain**     |
| ----------------------------- | ---------------------------------------------------------- | -------------------------- |
| **crontab -e**                | Current user ki crontab edit karta hai                     | Cron job add/edit karna    |
| **crontab -l**                | Current user ki cron jobs list karta hai                   | Existing crons dekhna      |
| **crontab -r**                | Current user ki saari cron jobs delete karta hai (CAREFUL) | Cron cleanup - be careful! |
| **crontab -u john -l**        | John user ki cron jobs list karta hai                      | Other user crons check     |
| **sudo crontab -e**           | Root user ki crontab edit karta hai                        | System-level cron          |
| **cat /etc/crontab**          | System-wide crontab file dikhata hai                       | System crons check         |
| **ls /etc/cron.d/**           | Application-specific cron files dikhata hai                | App crons location         |
| **ls /etc/cron.daily/**       | Daily cron scripts dikhata hai                             | Daily scheduled tasks      |
| **run-parts /etc/cron.daily** | Daily crons manually run karta hai                         | Manual cron trigger        |
| **grep CRON /var/log/syslog** | Cron execution logs check karta hai                        | Cron troubleshooting       |

# **10\. SSH & Remote Access**

SSH engineers ka lifeline hai. Secure remote access, file transfer, tunneling, key management - sab yahan cover hai.

## **10.1 SSH Connection**

| **Command / Syntax**                          | **Kya Karta Hai**                          | **Kyu Use Karte Hain**   |
| --------------------------------------------- | ------------------------------------------ | ------------------------ |
| **ssh user@host**                             | Remote server se connect karta hai         | Basic SSH login          |
| **ssh -p 2222 user@host**                     | Custom port pe connect karta hai           | Non-standard SSH port    |
| **ssh -i ~/.ssh/key.pem user@host**           | Specific private key use karta hai         | Key-based authentication |
| **ssh -v user@host**                          | Verbose mode - connection debug karta hai  | SSH troubleshooting      |
| **ssh -X user@host**                          | X11 forwarding enable karta hai (GUI apps) | Remote GUI run karna     |
| **ssh -A user@host**                          | Agent forwarding - keys chain karta hai    | Bastion host ke liye     |
| **ssh -N -L 8080:localhost:80 user@host**     | Local port forwarding                      | Remote service access    |
| **ssh -N -R 9090:localhost:80 user@host**     | Remote port forwarding                     | Expose local service     |
| **ssh -D 1080 user@host**                     | Dynamic SOCKS proxy banata hai             | Traffic tunneling        |
| **ssh -t user@bastion ssh user@internal**     | Jump host ke through access                | Bastion/jump server      |
| **ssh -J bastion user@internal**              | ProxyJump - modern jump host syntax        | Modern bastion access    |
| **ssh -o StrictHostKeyChecking=no user@host** | Host key check skip karta hai              | Automation mein use      |

## **10.2 SSH Key Management**

| **Command / Syntax**                                | **Kya Karta Hai**                                  | **Kyu Use Karte Hain**  |
| --------------------------------------------------- | -------------------------------------------------- | ----------------------- |
| **ssh-keygen -t rsa -b 4096**                       | 4096-bit RSA key pair generate karta hai           | Strong key create karna |
| **ssh-keygen -t ed25519**                           | ED25519 key generate karta hai (modern, preferred) | Best practice key       |
| **ssh-keygen -t ed25519 -C 'email'**                | Comment ke saath key generate karta hai            | Identifiable key        |
| **ssh-copy-id user@host**                           | Public key remote server pe copy karta hai         | Passwordless SSH setup  |
| **ssh-copy-id -i ~/.ssh/id_rsa.pub user@host**      | Specific key copy karta hai                        | Specific key deploy     |
| **cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys** | Manual key add karta hai                           | Manual authorized keys  |
| **chmod 400 ~/.ssh/id_rsa**                         | Private key sirf read-only (strictest)             | Stricter key protection |
| **chmod 644 ~/.ssh/id_rsa.pub**                     | Public key permissions set karta hai               | Public key permission   |
| **ssh-add ~/.ssh/id_rsa**                           | Key SSH agent mein add karta hai                   | Passphrase cache karna  |
| **ssh-add -l**                                      | Agent mein loaded keys list karta hai              | Loaded keys check       |
| **ssh-add -d ~/.ssh/id_rsa**                        | Agent se key remove karta hai                      | Key remove from agent   |
| **eval \$(ssh-agent -s)**                           | SSH agent start karta hai                          | Agent start karna       |
| **ssh-keyscan -H host >> known_hosts**              | Host fingerprint add karta hai                     | Automated known_hosts   |

## **10.3 SSH Config File**

| \# ~/.ssh/config file - SSH connections simplify karta hai |
| ---------------------------------------------------------- |
|                                                            |
| Host production                                            |
| HostName 203.0.113.10                                      |
| User ubuntu                                                |
| IdentityFile ~/.ssh/prod_key.pem                           |
| Port 22                                                    |
|                                                            |
| Host bastion                                               |
| HostName 203.0.113.1                                       |
| User ec2-user                                              |
| IdentityFile ~/.ssh/bastion.pem                            |
|                                                            |
| Host internal-server                                       |
| HostName 10.0.0.50                                         |
| User ubuntu                                                |
| ProxyJump bastion                                          |
| IdentityFile ~/.ssh/internal.pem                           |
|                                                            |
| \# Ab sirf: ssh production                                 |
| \# Jump server: ssh internal-server                        |

## **10.4 SCP & rsync - File Transfer**

| **Command / Syntax**                                  | **Kya Karta Hai**                               | **Kyu Use Karte Hain**  |
| ----------------------------------------------------- | ----------------------------------------------- | ----------------------- |
| **scp file.txt user@host:/remote/path**               | Local file remote pe copy karta hai             | File upload karna       |
| **scp user@host:/remote/file.txt ./**                 | Remote file local pe download karta hai         | File download karna     |
| **scp -r /local/dir user@host:/remote/**              | Directory recursively copy karta hai            | Folder upload karna     |
| **scp -P 2222 file user@host:/path**                  | Custom port pe SCP                              | Non-standard port SCP   |
| **scp -i key.pem file user@host:/path**               | Key-based SCP                                   | Secure SCP with key     |
| **rsync -avz /src/ user@host:/dst/**                  | Compressed incremental sync karta hai           | Efficient file sync     |
| **rsync -avz --delete /src/ user@host:/dst/**         | Destination se extra files bhi delete karta hai | Mirror sync             |
| **rsync -avz --progress /src/ /dst/**                 | Progress dikhata hai                            | Transfer progress       |
| **rsync -n /src/ user@host:/dst/**                    | Dry run - actually copy nahi karta              | Test rsync first        |
| **rsync -avz -e 'ssh -p 2222' /src/ user@host:/dst/** | Custom SSH port ke saath                        | Non-standard port rsync |
| **rsync --exclude='\*.log' /src/ /dst/**              | Log files exclude karta hai                     | Selective sync          |

# **11\. Shell Scripting - Bash**

Automation DevOps ka core hai aur Bash scripting uska foundation. Repetitive tasks automate karna, deployment scripts, health check scripts - sab Bash se hota hai.

## **11.1 Script Basics**

| #!/bin/bash # Shebang - bash interpreter use karo              |
| -------------------------------------------------------------- |
| set -e # Kisi bhi error pe script exit kar do                  |
| set -u # Undefined variable use hone pe exit karo              |
| set -o pipefail # Pipe failures bhi error mein count ho        |
| set -x # Debug mode - har command print karo                   |
|                                                                |
| \# Variables                                                   |
| NAME='Production' # String variable                            |
| PORT=8080 # Numeric variable                                   |
| FILES=\$(ls /etc/\*.conf) # Command output variable mein store |
| readonly MAX=100 # Read-only constant                          |
|                                                                |
| \# String operations                                           |
| echo \${#NAME} # String length                                 |
| echo \${NAME:0:4} # Substring (position 0, length 4)           |
| echo \${NAME,,} # Lowercase convert                            |
| echo \${NAME^^} # Uppercase convert                            |
| echo \${NAME/old/new} # Replace in string                      |
| echo \${VAR:-default} # Default value agar VAR unset ho        |
| echo \${VAR:=default} # Set aur use default agar VAR unset ho  |

## **11.2 Conditionals & Comparisons**

| \# If-else                                     |
| ---------------------------------------------- |
| if \[ condition \]; then                       |
| echo 'true'                                    |
| elif \[ other \]; then                         |
| echo 'other'                                   |
| else                                           |
| echo 'false'                                   |
| fi                                             |
|                                                |
| \# String comparisons                          |
| \[ "\$A" = "\$B" \] # Equal                    |
| \[ "\$A" != "\$B" \] # Not equal               |
| \[ -z "\$VAR" \] # Empty string hai            |
| \[ -n "\$VAR" \] # Non-empty string hai        |
|                                                |
| \# Numeric comparisons                         |
| \[ \$A -eq \$B \] # Equal                      |
| \[ \$A -ne \$B \] # Not equal                  |
| \[ \$A -gt \$B \] # Greater than               |
| \[ \$A -ge \$B \] # Greater than or equal      |
| \[ \$A -lt \$B \] # Less than                  |
| \[ \$A -le \$B \] # Less than or equal         |
|                                                |
| \# File tests                                  |
| \[ -f file \] # Regular file exist karta hai   |
| \[ -d dir \] # Directory exist karta hai       |
| \[ -e path \] # File/dir exist karta hai       |
| \[ -r file \] # Readable hai                   |
| \[ -w file \] # Writable hai                   |
| \[ -x file \] # Executable hai                 |
| \[ -s file \] # Non-empty file hai             |
| \[ file1 -nt file2 \] # file1 newer than file2 |
|                                                |
| \# Logical operators                           |
| \[\[ \$A && \$B \]\] # AND                     |
| \[\[ \$A \| \$B \]\] # OR                      |
| \[\[ ! \$A \]\] # NOT                          |

## **11.3 Loops**

| \# For loop - list iterate                  |
| ------------------------------------------- |
| for server in web1 web2 web3; do            |
| echo "Deploying to \$server"                |
| ssh \$server 'sudo systemctl restart myapp' |
| done                                        |
|                                             |
| \# For loop - range                         |
| for i in \$(seq 1 10); do                   |
| echo "Iteration \$i"                        |
| done                                        |
|                                             |
| \# C-style for loop                         |
| for ((i=0; i<5; i++)); do                   |
| echo \$i                                    |
| done                                        |
|                                             |
| \# While loop                               |
| COUNT=0                                     |
| while \[ \$COUNT -lt 5 \]; do               |
| echo "Count: \$COUNT"                       |
| ((COUNT++))                                 |
| done                                        |
|                                             |
| \# Until loop (opposite of while)           |
| until ping -c1 google.com; do               |
| echo 'Waiting for network...'               |
| sleep 5                                     |
| done                                        |
|                                             |
| \# Read file line by line                   |
| while IFS= read -r line; do                 |
| echo "Processing: \$line"                   |
| done < /etc/hosts                           |
|                                             |
| \# break aur continue                       |
| for i in 1 2 3 4 5; do                      |
| \[ \$i -eq 3 \] && continue # 3 skip karo   |
| \[ \$i -eq 5 \] && break # 5 pe stop karo   |
| echo \$i                                    |
| done                                        |

## **11.4 Functions & Error Handling**

| \# Function define karna                       |
| ---------------------------------------------- |
| check_service() {                              |
| local SERVICE=\$1 # Local variable             |
| local HOST=\${2:-localhost} # Default value    |
|                                                |
| if systemctl is-active --quiet \$SERVICE; then |
| echo "\$SERVICE is running"                    |
| return 0                                       |
| else                                           |
| echo "ERROR: \$SERVICE is DOWN!"               |
| return 1                                       |
| fi                                             |
| }                                              |
|                                                |
| \# Function call karna                         |
| check_service nginx                            |
| check_service mysql db-server                  |
|                                                |
| \# Return value check                          |
| if check_service nginx; then                   |
| echo 'All good'                                |
| else                                           |
| echo 'Service failed!'                         |
| exit 1                                         |
| fi                                             |
|                                                |
| \# Exit codes                                  |
| \# 0 = success, non-zero = failure             |
| echo "Last command exit code: \$?"             |
|                                                |
| \# Trap - cleanup on exit/error                |
| cleanup() {                                    |
| echo 'Cleaning up...'                          |
| rm -f /tmp/lock.\$\$                           |
| }                                              |
| trap cleanup EXIT # Script exit pe cleanup     |
| trap cleanup ERR # Error pe cleanup            |
| trap 'echo Ctrl+C!' INT # Ctrl+C catch karna   |

## **11.5 Arrays & Advanced Features**

| \# Array declare karna                                                 |
| ---------------------------------------------------------------------- |
| SERVERS=('web1' 'web2' 'db1' 'cache1')                                 |
|                                                                        |
| \# Array access                                                        |
| echo \${SERVERS\[0\]} # First element: web1                            |
| echo \${SERVERS\[-1\]} # Last element: cache1                          |
| echo \${SERVERS\[@\]} # Saare elements                                 |
| echo \${#SERVERS\[@\]} # Array length                                  |
|                                                                        |
| \# Array iterate                                                       |
| for srv in "\${SERVERS\[@\]}"; do                                      |
| echo "Checking \$srv"                                                  |
| done                                                                   |
|                                                                        |
| \# Associative array (dictionary)                                      |
| declare -A PORTS                                                       |
| PORTS\[nginx\]=80                                                      |
| PORTS\[mysql\]=3306                                                    |
| PORTS\[redis\]=6379                                                    |
|                                                                        |
| for svc in "\${!PORTS\[@\]}"; do                                       |
| echo "\$svc runs on port \${PORTS\[\$svc\]}"                           |
| done                                                                   |
|                                                                        |
| \# Command line arguments                                              |
| \# \$0 = script name, \$1 = first arg, \$@ = all args, \$# = arg count |
| echo "Script: \$0, Args: \$@, Count: \$#"                              |
|                                                                        |
| \# Input validation                                                    |
| if \[ \$# -lt 2 \]; then                                               |
| echo "Usage: \$0 &lt;environment&gt; &lt;version&gt;"                  |
| exit 1                                                                 |
| fi                                                                     |
| ENV=\$1                                                                |
| VERSION=\$2                                                            |

# **12\. Package Management**

Software install, update, remove karna - ye daily task hai. Ubuntu/Debian mein apt, RHEL/CentOS mein yum/dnf use hota hai. Dono cover kiye gaye hain.

## **12.1 APT - Debian/Ubuntu**

| **Command / Syntax**                  | **Kya Karta Hai**                             | **Kyu Use Karte Hain**   |
| ------------------------------------- | --------------------------------------------- | ------------------------ |
| **apt update**                        | Package repository list update karta hai      | Install se pehle ZAROORI |
| **apt upgrade**                       | Saare packages upgrade karta hai              | System update karna      |
| **apt full-upgrade**                  | Dependencies bhi update karta hai             | Complete upgrade         |
| **apt install nginx**                 | nginx install karta hai                       | Package install          |
| **apt install -y nginx**              | Auto yes - scripting ke liye                  | Unattended install       |
| **apt install nginx=1.18.0-0ubuntu1** | Specific version install karta hai            | Version pinning          |
| **apt remove nginx**                  | Package remove karta hai (configs rakhta hai) | Package uninstall        |
| **apt purge nginx**                   | Package + config files remove karta hai       | Complete removal         |
| **apt autoremove**                    | Unused dependencies remove karta hai          | Cleanup orphan packages  |
| **apt search keyword**                | Package search karta hai                      | Package dhundna          |
| **apt show nginx**                    | Package details dikhata hai                   | Package info check       |
| **apt list --installed**              | Installed packages list karta hai             | Installed audit          |
| **apt list --upgradable**             | Upgradable packages list karta hai            | Update check             |
| **dpkg -l**                           | All installed packages list karta hai         | Complete package list    |
| **dpkg -l \| grep nginx**             | Specific package installed hai check          | Package verify           |
| **dpkg -i package.deb**               | Local .deb file install karta hai             | Manual deb install       |
| **dpkg --get-selections > pkgs.txt**  | Installed packages export karta hai           | Package list backup      |

## **12.2 YUM/DNF - RHEL/CentOS/Fedora**

| **Command / Syntax**     | **Kya Karta Hai**                         | **Kyu Use Karte Hain**     |
| ------------------------ | ----------------------------------------- | -------------------------- |
| **dnf update**           | Saare packages update karta hai           | System update (modern)     |
| **yum update**           | Legacy update command (older systems)     | CentOS 7 update            |
| **dnf install nginx**    | nginx install karta hai                   | Package install            |
| **dnf remove nginx**     | Package remove karta hai                  | Package uninstall          |
| **dnf search keyword**   | Package search karta hai                  | Package dhundna            |
| **dnf info nginx**       | Package information dikhata hai           | Package details            |
| **dnf list installed**   | Installed packages list karta hai         | Installed audit            |
| **dnf history**          | Package transaction history dikhata hai   | What was installed/removed |
| **dnf history undo 5**   | Transaction 5 undo karta hai              | Rollback package change    |
| **rpm -qa**              | All installed RPM packages list karta hai | Complete RPM list          |
| **rpm -qi nginx**        | nginx package info dikhata hai            | Package details            |
| **rpm -ql nginx**        | nginx ke installed files list karta hai   | Package files list         |
| **rpm -ivh package.rpm** | Local RPM install karta hai               | Manual RPM install         |

# **13\. File Searching - find, locate, which, whereis**

Production mein files dhundna ek common task hai - config files, log files, large files, recently modified files. find ek very powerful tool hai.

## **13.1 find - Powerful File Search**

| **Command / Syntax**                                   | **Kya Karta Hai**                           | **Kyu Use Karte Hain**        |
| ------------------------------------------------------ | ------------------------------------------- | ----------------------------- |
| **find / -name 'nginx.conf'**                          | Poore system mein nginx.conf dhundta hai    | File location find            |
| **find /etc -name '\*.conf'**                          | /etc mein saari .conf files                 | Config files list             |
| **find . -name '\*.log' -type f**                      | Current dir mein log files                  | Log files find                |
| **find /var -type d**                                  | Sirf directories list karta hai             | Directory list                |
| **find /var -type l**                                  | Symbolic links list karta hai               | Symlinks find                 |
| **find . -mtime -7**                                   | Last 7 days mein modified files             | Recent changes find           |
| **find . -mtime +30**                                  | 30 days se purani files                     | Old files find                |
| **find . -newer reference.txt**                        | reference.txt se newer files                | Newer than file               |
| **find /var/log -size +100M**                          | 100MB se badi files                         | Large files find              |
| **find / -size +1G -type f**                           | 1GB se badi files poore system mein         | Disk space hogs               |
| **find . -empty**                                      | Empty files aur directories                 | Empty files find              |
| **find /home -perm 777**                               | 777 permissions wali files (security risk!) | Security audit                |
| **find /etc -perm /222**                               | World-writable files dhundta hai            | Write permission audit        |
| **find . -user john**                                  | John user ki files                          | User files find               |
| **find . -group developers**                           | developers group ki files                   | Group files find              |
| **find . -name '\*.tmp' -delete**                      | Temporary files dhundhke delete karta hai   | Automated cleanup             |
| **find . -name '\*.log' -exec gzip {} \\;**            | Log files dhundhke compress karta hai       | Bulk operation                |
| **find . -name '\*.conf' -exec grep -l 'port' {} \\;** | Config files mein port dhundta hai          | Content search in found files |
| **find /proc -maxdepth 1 -type d -name '\[0-9\]\*'**   | Running process directories                 | Process enumeration           |

## **13.2 locate, which, whereis, type**

| **Command / Syntax**  | **Kya Karta Hai**                              | **Kyu Use Karte Hain**  |
| --------------------- | ---------------------------------------------- | ----------------------- |
| **locate nginx.conf** | Database se file quickly dhundta hai           | Fast file search        |
| **locate -i nginx**   | Case-insensitive locate search                 | Case-insensitive search |
| **updatedb**          | locate database update karta hai (sudo)        | Database refresh        |
| **which python3**     | Command ka full path nikalta hai               | Executable location     |
| **which -a python**   | Saare matching executables path dikhata hai    | All executable paths    |
| **whereis nginx**     | Binary, source, man page locations dikhata hai | Complete tool info      |
| **type ls**           | Command type dikhata hai (alias/builtin/file)  | Command type check      |
| **type -a ls**        | Saare matching command types                   | All type definitions    |
| **command -v docker** | Command exist karta hai ya nahi (scripting)    | Command existence check |

# **14\. Environment Variables & Shell Configuration**

## **14.1 Environment Variables**

| **Command / Syntax**        | **Kya Karta Hai**                                           | **Kyu Use Karte Hain**    |
| --------------------------- | ----------------------------------------------------------- | ------------------------- |
| **env**                     | Saare environment variables dikhata hai                     | Current environment check |
| **printenv**                | Environment variables print karta hai                       | Env variables list        |
| **printenv PATH**           | PATH variable value dikhata hai                             | PATH check karna          |
| **echo \$HOME**             | HOME variable value print karta hai                         | Home dir check            |
| **export MY_VAR=value**     | Variable set karke child processes ke liye export karta hai | Env var set karna         |
| **export -p**               | Saare exported variables dikhata hai                        | Exported vars list        |
| **unset MY_VAR**            | Variable unset karta hai                                    | Env var remove karna      |
| **MY_VAR=val command**      | Sirf uss command ke liye variable set karta hai             | Temporary env var         |
| **source /etc/environment** | File se variables current shell mein load karta hai         | Env file reload karna     |
| **. ~/.bashrc**             | . (dot) se source karta hai (same as source)                | Bashrc reload             |
| **PATH=\$PATH:/new/path**   | PATH mein naya directory add karta hai                      | Custom binary path add    |

## **14.2 Important System Variables**

| **Command / Syntax** | **Kya Karta Hai**                                     | **Kyu Use Karte Hain**  |
| -------------------- | ----------------------------------------------------- | ----------------------- |
| **\$PATH**           | Executables dhundne ki directories list               | Command path resolution |
| **\$HOME**           | Current user ka home directory                        | Home dir reference      |
| **\$USER**           | Current logged-in username                            | User identification     |
| **\$SHELL**          | Current shell path                                    | Shell check             |
| **\$PWD**            | Current working directory                             | Like 'pwd' command      |
| **\$OLDPWD**         | Previous working directory                            | 'cd -' functionality    |
| **\$HOSTNAME**       | Current machine hostname                              | Server identification   |
| **\$?**              | Last command ka exit code                             | Success/failure check   |
| **\$\$**             | Current shell ka PID                                  | Unique temp filenames   |
| **\$!**              | Last background process ka PID                        | Background job tracking |
| **\$0**              | Script/shell ka naam                                  | Script self-reference   |
| **\$1..\$9**         | Script ke positional arguments                        | Argument parsing        |
| **\$@**              | Saare arguments (separate words)                      | All args iteration      |
| **\$#**              | Arguments ki count                                    | Arg count validation    |
| **\$IFS**            | Internal Field Separator (default: space,tab,newline) | Word splitting control  |
| **\$RANDOM**         | Random number 0-32767                                 | Random value in scripts |
| **\$LINENO**         | Current script line number                            | Debug output mein       |

## **14.3 Shell Config Files**

| **Command / Syntax** | **Kya Karta Hai**                            | **Kyu Use Karte Hain**   |
| -------------------- | -------------------------------------------- | ------------------------ |
| **/etc/profile**     | Login shells ke liye system-wide settings    | System-wide env setup    |
| **/etc/bashrc**      | Interactive non-login shells ke liye         | System bash config       |
| **/etc/environment** | System-wide env variables (non-shell format) | System env variables     |
| **~/.bashrc**        | User ke interactive non-login shell config   | User bash customization  |
| **~/.bash_profile**  | User ke login shell config                   | User login setup         |
| **~/.bash_aliases**  | Aliases define karne ki file                 | Custom command shortcuts |
| **~/.profile**       | Login shell config (POSIX sh compatible)     | Cross-shell login config |
| **~/.bash_history**  | Command history file                         | Previous commands stored |
| **~/.ssh/config**    | SSH connection configurations                | SSH shortcuts define     |

# **15\. Pipelines, I/O Redirection & xargs**

Linux ki real power pipes aur redirection mein hai. Complex tasks chhote commands ko combine karke achieve hote hain - ye Unix philosophy ka core hai.

## **15.1 I/O Redirection**

| **Command / Syntax**        | **Kya Karta Hai**                               | **Kyu Use Karte Hain**      |
| --------------------------- | ----------------------------------------------- | --------------------------- |
| **command > file**          | STDOUT file mein redirect karta hai (overwrite) | Output file mein save karna |
| **command >> file**         | STDOUT file mein append karta hai               | Output file mein add karna  |
| **command 2> error.log**    | STDERR error.log mein redirect karta hai        | Error log separate karna    |
| **command 2>> error.log**   | STDERR append karta hai                         | Error log append karna      |
| **command &> all.log**      | STDOUT + STDERR dono ek file mein               | All output capture          |
| **command >> out.log 2>&1** | STDERR ko STDOUT ke saath merge karta hai       | Combined logging            |
| **command 2>/dev/null**     | Errors /dev/null mein discard karta hai         | Error output suppress       |
| **command >/dev/null 2>&1** | Saara output suppress karta hai                 | Silent execution            |
| **command < input.txt**     | File se input read karta hai                    | File as STDIN               |
| **command << EOF**          | Here document - multiline inline input          | Multiline input             |
| **command <<< 'string'**    | Here string - single string as STDIN            | Quick string input          |

## **15.2 Pipes & Chaining**

| **Command / Syntax**                  | **Kya Karta Hai**                                                 | **Kyu Use Karte Hain**   |
| ------------------------------------- | ----------------------------------------------------------------- | ------------------------ |
| **cmd1 \| cmd2**                      | cmd1 output cmd2 ka input ban jaata hai                           | Command pipeline         |
| **cmd1 ; cmd2**                       | cmd1 ke baad cmd2 run karta hai (regardless of success)           | Sequential commands      |
| **cmd1 && cmd2**                      | cmd2 sirf tab run karta hai jab cmd1 success ho                   | Conditional execution    |
| **cmd1 \| cmd2**                      | cmd2 sirf tab run karta hai jab cmd1 fail ho                      | Fallback command         |
| **tee file.txt**                      | Output screen pe bhi dikhata hai aur file mein bhi save karta hai | Output fork karna        |
| **tee -a file.txt**                   | tee append mode mein                                              | Append while viewing     |
| **cmd1 \| tee mid.log \| cmd2**       | Middle mein output capture karta hai                              | Pipeline inspection      |
| **xargs command**                     | STDIN se arguments leke command run karta hai                     | Bulk command execution   |
| **find . -name '\*.log' \| xargs rm** | Found files delete karta hai                                      | Find + bulk delete       |
| **cat hosts.txt \| xargs ping -c1**   | File mein listed hosts ping karta hai                             | Bulk operations          |
| **xargs -n1 command**                 | Ek ek argument se command run karta hai                           | One-by-one processing    |
| **xargs -P4 command**                 | 4 parallel processes run karta hai                                | Parallel execution       |
| **xargs -I{} cp {} /dst/**            | {} se argument place karta hai                                    | Custom argument position |

## **15.3 Useful Pipeline Combinations**

| \# Top 10 largest files                                                                |
| -------------------------------------------------------------------------------------- |
| du -ah /var \| sort -rh \| head -10                                                    |
|                                                                                        |
| \# Most frequent log errors                                                            |
| grep 'ERROR' app.log \| awk '{print \$NF}' \| sort \| uniq -c \| sort -rn \| head -20  |
|                                                                                        |
| \# Active connections count by state                                                   |
| ss -ta \| awk '{print \$1}' \| sort \| uniq -c \| sort -rn                             |
|                                                                                        |
| \# Disk space check + alert                                                            |
| df -h \| grep -v tmpfs \| awk '\$5 > "80%" {print "ALERT: "\$6" is "\$5" full"}'       |
|                                                                                        |
| \# Find and compress old logs                                                          |
| find /var/log -name '\*.log' -mtime +7 \| xargs gzip                                   |
|                                                                                        |
| \# Count unique IPs in access log                                                      |
| awk '{print \$1}' /var/log/nginx/access.log \| sort \| uniq -c \| sort -rn \| head -20 |
|                                                                                        |
| \# Remove duplicate lines while preserving order                                       |
| awk '!seen\[\$0\]++' file.txt                                                          |
|                                                                                        |
| \# Check all services status                                                           |
| systemctl list-units --type=service --state=active \| awk '{print \$1}'                |

# **16\. Archive & Compression**

## **16.1 tar - Tape Archive**

| **Command / Syntax**                                 | **Kya Karta Hai**                                    | **Kyu Use Karte Hain**    |
| ---------------------------------------------------- | ---------------------------------------------------- | ------------------------- |
| **tar -czf archive.tar.gz /path/**                   | Directory ko gzip compress karke archive karta hai   | Backup banana - MOST USED |
| **tar -cjf archive.tar.bz2 /path/**                  | bzip2 compression ke saath archive                   | Better compression        |
| **tar -cJf archive.tar.xz /path/**                   | xz compression (best ratio) ke saath                 | Maximum compression       |
| **tar -czf backup.tar.gz --exclude='\*.log' /path/** | Log files exclude karke backup                       | Selective backup          |
| **tar -tzf archive.tar.gz**                          | Archive contents list karta hai (extract nahi karta) | Archive contents check    |
| **tar -xzf archive.tar.gz**                          | gzip archive extract karta hai                       | Archive extract karna     |
| **tar -xzf archive.tar.gz -C /dest/**                | Specific directory mein extract karta hai            | Custom extract location   |
| **tar -xzf archive.tar.gz file.txt**                 | Specific file sirf extract karta hai                 | Single file extract       |
| **tar -xvzf archive.tar.gz**                         | Verbose extract - files naam dikhata hai             | Debug extraction          |
| **tar -rf archive.tar file**                         | Existing archive mein file add karta hai             | Archive mein add karna    |

## **16.2 gzip, bzip2, zip, xz**

| **Command / Syntax**            | **Kya Karta Hai**                                  | **Kyu Use Karte Hain**      |
| ------------------------------- | -------------------------------------------------- | --------------------------- |
| **gzip file.txt**               | file.txt compress karke file.txt.gz banata hai     | Quick compression           |
| **gzip -k file.txt**            | Original file preserve karta hai                   | Keep original               |
| **gzip -d file.txt.gz**         | gzip file decompress karta hai                     | Decompress                  |
| **gunzip file.txt.gz**          | gunzip se decompress karta hai (same as gzip -d)   | Alternative decompress      |
| **gzip -l file.txt.gz**         | Compression ratio dikhata hai                      | Compression stats           |
| **bzip2 file.txt**              | bzip2 se compress karta hai (better ratio, slower) | Better compression          |
| **bunzip2 file.txt.bz2**        | bzip2 file decompress karta hai                    | bzip2 decompress            |
| **zip archive.zip files**       | Zip archive banata hai                             | Zip format (Windows compat) |
| **zip -r archive.zip dir/**     | Directory ko recursively zip karta hai             | Directory zip               |
| **unzip archive.zip**           | Zip archive extract karta hai                      | Zip extract                 |
| **unzip -l archive.zip**        | Zip contents list karta hai                        | Zip contents check          |
| **unzip archive.zip -d /dest/** | Specific directory mein extract karta hai          | Custom unzip location       |
| **xz file**                     | xz compression (best ratio)                        | Maximum compression         |
| **xz -d file.xz**               | xz decompress karta hai                            | xz decompress               |
| **zcat file.gz**                | gz file bina extract kiye read karta hai           | Compressed file read        |
| **zless file.gz**               | gz file bina extract kiye page-by-page padhta hai  | Compressed log read         |
| **zgrep 'pattern' file.gz**     | gz file mein grep karta hai                        | Compressed log search       |

# **17\. User & Group Management**

## **17.1 User Management**

| **Command / Syntax**                | **Kya Karta Hai**                             | **Kyu Use Karte Hain** |
| ----------------------------------- | --------------------------------------------- | ---------------------- |
| **useradd john**                    | User john create karta hai                    | New user add karna     |
| **useradd -m -s /bin/bash john**    | Home dir + bash shell ke saath user create    | Full user creation     |
| **useradd -u 1500 -g devs john**    | Specific UID aur group ke saath user create   | Custom UID/GID user    |
| **useradd -M john**                 | Home directory create nahi karta              | Service account create |
| **useradd -r -s /sbin/nologin svc** | System/service user create karta hai          | Service account        |
| **passwd john**                     | John ka password set/change karta hai         | Password management    |
| **passwd -l john**                  | John ka account lock karta hai                | Account disable karna  |
| **passwd -u john**                  | John ka account unlock karta hai              | Account re-enable      |
| **passwd -e john**                  | Password expire - next login pe change forced | Force password change  |
| **usermod -aG docker john**         | John ko docker group mein add karta hai       | Group add karna        |
| **usermod -s /bin/zsh john**        | John ka shell change karta hai                | Shell change           |
| **usermod -L john**                 | Account lock karta hai (login disable)        | Lock account           |
| **usermod -U john**                 | Account unlock karta hai                      | Unlock account         |
| **usermod -d /new/home -m john**    | Home directory move karta hai                 | Home dir change        |
| **userdel john**                    | User delete karta hai (home dir rakhta hai)   | User remove            |
| **userdel -r john**                 | User + home directory dono delete karta hai   | Complete user removal  |
| **id john**                         | John ka UID, GID, groups dikhata hai          | User identity info     |
| **finger john**                     | User information dikhata hai                  | User details           |
| **lastlog**                         | Saare users ka last login time dikhata hai    | Last login audit       |
| **whoami**                          | Current user ka naam dikhata hai              | Identity quick check   |
| **users**                           | Currently logged-in usernames dikhata hai     | Logged in users list   |

## **17.2 Group Management**

| **Command / Syntax**            | **Kya Karta Hai**                            | **Kyu Use Karte Hain** |
| ------------------------------- | -------------------------------------------- | ---------------------- |
| **groupadd developers**         | developers group create karta hai            | New group banana       |
| **groupadd -g 2000 devteam**    | Specific GID ke saath group create karta hai | Custom GID group       |
| **groupmod -n devs developers** | Group rename karta hai                       | Group rename           |
| **groupdel developers**         | Group delete karta hai                       | Group remove           |
| **gpasswd -a john developers**  | John ko developers group mein add karta hai  | Group member add       |
| **gpasswd -d john developers**  | John ko developers group se remove karta hai | Group member remove    |
| **gpasswd -M john,jane devs**   | Group ke saare members set karta hai         | Bulk group members     |
| **groups john**                 | John ki saari group memberships dikhata hai  | User groups check      |
| **cat /etc/group**              | Saare groups aur members dikhata hai         | Groups file view       |
| **getent group developers**     | developers group info nikalta hai            | Group details          |

# **18\. DevOps/SRE Specific Tools & Commands**

Ye section un commands pe focus karta hai jo specifically DevOps, Platform Engineering aur SRE roles mein daily use hote hain.

## **18.1 curl - API Testing & HTTP**

| **Command / Syntax**                                                        | **Kya Karta Hai**                     | **Kyu Use Karte Hain**  |
| --------------------------------------------------------------------------- | ------------------------------------- | ----------------------- |
| **curl <https://api.example.com>**                                          | GET request karta hai                 | API call karna          |
| **curl -X POST -d '{"key":"val"}' -H 'Content-Type: application/json' URL** | JSON POST request                     | API POST call           |
| **curl -X DELETE <https://api.com/items/1>**                                | DELETE request karta hai              | API resource delete     |
| **curl -u user:pass URL**                                                   | Basic auth ke saath request           | Basic authentication    |
| **curl -H 'Authorization: Bearer TOKEN' URL**                               | Bearer token auth                     | OAuth/JWT auth          |
| **curl -o output.json URL**                                                 | Response file mein save karta hai     | Response save karna     |
| **curl -s URL \| python3 -m json.tool**                                     | JSON response pretty print karta hai  | JSON debugging          |
| **curl --max-time 10 URL**                                                  | 10 second timeout set karta hai       | Timeout control         |
| **curl -w '%{http_code}' -o /dev/null -s URL**                              | Sirf HTTP status code dikhata hai     | Health check scripts    |
| **curl -k <https://self-signed.example.com>**                               | SSL certificate verify skip karta hai | Self-signed cert bypass |
| **curl --resolve host:443:IP URL**                                          | Specific IP pe resolve karta hai      | DNS override karna      |
| **curl -x proxy:8080 URL**                                                  | Proxy ke through request karta hai    | Proxy debugging         |

## **18.2 netcat (nc) & socat**

| **Command / Syntax**                          | **Kya Karta Hai**                           | **Kyu Use Karte Hain** |
| --------------------------------------------- | ------------------------------------------- | ---------------------- |
| **nc -l 8080**                                | Port 8080 pe listen karta hai               | Quick TCP server       |
| **nc host 8080**                              | host:8080 se TCP connect karta hai          | TCP client connect     |
| **nc -zv host 22**                            | SSH port 22 open hai check karta hai        | SSH port check         |
| **nc -zu host 53**                            | UDP port 53 check karta hai                 | UDP port check         |
| **echo 'PING' \| nc host 8080**               | Message bhejke response check karta hai     | Service response test  |
| **nc -l 9999 > received.txt**                 | Data receive karke file mein save karta hai | File transfer receive  |
| **nc host 9999 < send.txt**                   | File ke contents bhejta hai                 | File transfer send     |
| **socat TCP-LISTEN:8080,fork TCP:backend:80** | Port forwarding karta hai                   | Port proxy setup       |

## **18.3 strace & ltrace - System Call Tracing**

| **Command / Syntax**        | **Kya Karta Hai**                                    | **Kyu Use Karte Hain**  |
| --------------------------- | ---------------------------------------------------- | ----------------------- |
| **strace command**          | System calls trace karta hai                         | Debug failing command   |
| **strace -p 1234**          | Running process 1234 ke system calls trace karta hai | Attach to process       |
| **strace -e open command**  | Sirf 'open' system calls dikhata hai                 | Specific syscall filter |
| **strace -o trace.log cmd** | Trace output file mein save karta hai                | Trace logging           |
| **ltrace command**          | Library calls trace karta hai                        | Library debugging       |
| **strace -c command**       | System call statistics dikhata hai                   | Performance profiling   |

## **18.4 lsof - Open Files & Network**

| **Command / Syntax**                   | **Kya Karta Hai**                            | **Kyu Use Karte Hain** |
| -------------------------------------- | -------------------------------------------- | ---------------------- |
| **lsof**                               | Saare open files list karta hai (verbose!)   | Open files audit       |
| **lsof -p 1234**                       | PID 1234 ke open files aur sockets           | Process file audit     |
| **lsof +D /var/log/nginx**             | Directory ke andar open files wale processes | Directory open files   |
| **lsof -c nginx**                      | nginx process ke open files                  | App files check        |
| **lsof /var/log/nginx.log**            | Specific file open karne wale processes      | File usage check       |
| **lsof +D /var/log/**                  | Directory mein open files                    | Directory usage        |
| **lsof -i :8080**                      | Port 8080 use karne wale processes           | Port owner find        |
| **lsof -i tcp:80-8080**                | TCP port range use karne wale                | Port range check       |
| **lsof -i @192.168.1.1**               | Specific IP se connections                   | IP connection check    |
| **lsof -nP -i tcp -s tcp:ESTABLISHED** | Established TCP connections                  | Active connections     |

## **18.5 tcpdump - Network Packet Analysis**

| **Command / Syntax**                   | **Kya Karta Hai**                           | **Kyu Use Karte Hain**     |
| -------------------------------------- | ------------------------------------------- | -------------------------- |
| **tcpdump**                            | All interfaces pe packets capture karta hai | Basic packet capture       |
| **tcpdump -i eth0**                    | eth0 interface pe capture karta hai         | Interface specific capture |
| **tcpdump -i eth0 port 80**            | Port 80 ka traffic capture karta hai        | HTTP traffic capture       |
| **tcpdump -i eth0 host 8.8.8.8**       | Specific host ka traffic capture            | Host traffic capture       |
| **tcpdump -i eth0 -w capture.pcap**    | Packets file mein save karta hai            | Wireshark ke liye capture  |
| **tcpdump -r capture.pcap**            | pcap file read karta hai                    | Saved capture read         |
| **tcpdump -i eth0 'tcp and port 443'** | HTTPS traffic filter karta hai              | Protocol+port filter       |
| **tcpdump -i eth0 -n**                 | DNS resolve nahi karta (faster)             | Quick capture              |
| **tcpdump -i eth0 -A port 80**         | HTTP content ASCII mein dikhata hai         | HTTP content inspect       |
| **tcpdump -c 100 -i eth0**             | 100 packets capture karke stop karta hai    | Limited capture            |

# **19\. Security & System Hardening**

## **19.1 File Integrity & Checksums**

| **Command / Syntax**          | **Kya Karta Hai**                               | **Kyu Use Karte Hain** |
| ----------------------------- | ----------------------------------------------- | ---------------------- |
| **md5sum file.txt**           | MD5 checksum generate karta hai                 | File integrity check   |
| **md5sum -c checksums.md5**   | Checksum file se verify karta hai               | Batch integrity verify |
| **sha256sum file.txt**        | SHA-256 checksum generate karta hai (preferred) | Secure file verify     |
| **sha256sum -c SHA256SUMS**   | SHA-256 checksums verify karta hai              | Download verify        |
| **sha512sum file.txt**        | SHA-512 checksum (strongest)                    | High-security verify   |
| **openssl dgst -sha256 file** | OpenSSL se SHA-256 checksum                     | OpenSSL alternative    |

## **19.2 OpenSSL - Certificates & Encryption**

| **Command / Syntax**                                                                  | **Kya Karta Hai**                               | **Kyu Use Karte Hain** |
| ------------------------------------------------------------------------------------- | ----------------------------------------------- | ---------------------- |
| **openssl version**                                                                   | OpenSSL version check karta hai                 | OpenSSL info           |
| **openssl req -new -x509 -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem**   | Self-signed cert create karta hai               | Dev SSL cert           |
| **openssl x509 -in cert.pem -text -noout**                                            | Certificate details dikhata hai                 | Cert inspection        |
| **openssl x509 -in cert.pem -noout -enddate**                                         | Certificate expiry date dikhata hai             | Cert expiry check      |
| **openssl s_client -connect host:443**                                                | SSL/TLS connection test karta hai               | SSL debugging          |
| **openssl s_client -connect host:443 -servername host**                               | SNI ke saath SSL test karta hai                 | Virtual host SSL test  |
| **echo \| openssl s_client -connect h:443 2>/dev/null \| openssl x509 -noout -dates** | Quick cert dates                                | Cert validity check    |
| **openssl rsa -in key.pem -check**                                                    | Private key validate karta hai                  | Key validation         |
| **openssl enc -aes-256-cbc -in file -out encrypted**                                  | File encrypt karta hai                          | File encryption        |
| **openssl enc -d -aes-256-cbc -in encrypted -out decrypted**                          | File decrypt karta hai                          | File decryption        |
| **openssl rand -base64 32**                                                           | Random 32-byte base64 string generate karta hai | Secret key generate    |
| **openssl passwd -6 'mypassword'**                                                    | SHA-512 password hash generate karta hai        | Password hashing       |

## **19.3 Security Audit Commands**

| **Command / Syntax**                                                           | **Kya Karta Hai**                                  | **Kyu Use Karte Hain**  |
| ------------------------------------------------------------------------------ | -------------------------------------------------- | ----------------------- |
| **last \| head -20**                                                           | Recent logins dikhata hai                          | Login audit             |
| **lastb \| head -20**                                                          | Failed login attempts (brute force check)          | Security breach check   |
| **grep 'Failed password' /var/log/auth.log \| tail -20**                       | Failed SSH attempts                                | SSH attack monitoring   |
| **grep 'Accepted' /var/log/auth.log \| tail -20**                              | Successful SSH logins                              | Successful login audit  |
| **cat /etc/sudoers**                                                           | Sudo permissions check karta hai                   | Privilege audit         |
| **find / -perm -4000 -type f**                                                 | SetUID files dhundta hai (potential security risk) | SUID audit              |
| **find / -perm -2000 -type f**                                                 | SetGID files dhundta hai                           | SGID audit              |
| **find / -perm -0002 -type f**                                                 | World-writable files dhundta hai                   | World-write audit       |
| **netstat -an \| grep LISTEN**                                                 | Listening ports audit karta hai                    | Open port audit         |
| **arp -n**                                                                     | ARP table dikhata hai                              | Network neighbors       |
| **ss -tnp state established**                                                  | Sirf established TCP connections with process      | Active connection audit |
| **chage -l john**                                                              | John ki password aging info dikhata hai            | Password policy check   |
| **cat /etc/passwd \| awk -F: '\$7 != "/sbin/nologin" && \$7 != "/bin/false"'** | Login-capable users                                | User audit              |

# **20\. Production Troubleshooting Cheatsheet**

Ye section common production issues aur unhe troubleshoot karne ka systematic approach deta hai. Incident ke time yahi commands use hoti hain.

## **20.1 High CPU Troubleshooting**

| \# Step 1: CPU hog identify karo                       |
| ------------------------------------------------------ |
| top -b -n 1 \| head -20                                |
| ps aux --sort=-%cpu \| head -15                        |
|                                                        |
| \# Step 2: Specific process analyze karo               |
| PID=&lt;problematic_pid&gt;                            |
| cat /proc/\$PID/status # Process status                |
| cat /proc/\$PID/cmdline \| tr '\\0' ' ' # Full command |
| ls -la /proc/\$PID/fd \| head -20 # Open files         |
|                                                        |
| \# Step 3: System-level CPU analysis                   |
| mpstat -P ALL 1 5 # Per-CPU breakdown                  |
| vmstat 1 10 # CPU + IO + memory                        |
| sar -u 1 10 # CPU utilization history                  |
|                                                        |
| \# Step 4: Process ke threads dekhna                   |
| top -H -p \$PID                                        |
| ps -T -p \$PID                                         |

## **20.2 High Memory Troubleshooting**

| \# Step 1: Memory overview                                                       |
| -------------------------------------------------------------------------------- |
| free -h                                                                          |
| cat /proc/meminfo \| grep -E 'MemTotal\|MemFree\|MemAvailable\|Cached\|SwapUsed' |
|                                                                                  |
| \# Step 2: Memory hog find karo                                                  |
| ps aux --sort=-%mem \| head -15                                                  |
| top -b -n 1 \| sort -k 6 -rn \| head -20                                         |
|                                                                                  |
| \# Step 3: OOM killer check karo                                                 |
| dmesg \| grep -i 'oom\\\|killed process' \| tail -20                             |
| journalctl -k \| grep -i 'oom' \| tail -20                                       |
|                                                                                  |
| \# Step 4: Memory per process                                                    |
| cat /proc/\$PID/status \| grep -i vmrss                                          |
| pmap -x \$PID \| tail -5                                                         |

## **20.3 Disk Space Troubleshooting**

| \# Step 1: Space check karo                                                |
| -------------------------------------------------------------------------- |
| df -h                                                                      |
| df -i # Inode usage bhi check karo                                         |
|                                                                            |
| \# Step 2: Space hog identify karo                                         |
| du -sh /\* 2>/dev/null \| sort -rh \| head -15                             |
| du -sh /var/\* \| sort -rh \| head -10                                     |
| du -sh /var/log/\* \| sort -rh \| head -10                                 |
|                                                                            |
| \# Step 3: Large files dhundho                                             |
| find / -size +500M -type f 2>/dev/null \| sort                             |
| find / -size +1G -type f 2>/dev/null                                       |
|                                                                            |
| \# Step 4: Deleted but open files (disk space hold kar rahe hain)          |
| lsof \| grep '(deleted)' \| awk '{print \$7, \$9}' \| sort -rn \| head -10 |
| \# Process kill karo ya restart karo to release space                      |

## **20.4 Network Connectivity Troubleshooting**

| \# Step 1: Interface status check karo               |
| ---------------------------------------------------- |
| ip addr                                              |
| ip link                                              |
|                                                      |
| \# Step 2: Routing check karo                        |
| ip route                                             |
| ip route get 8.8.8.8 # Specific destination ka route |
|                                                      |
| \# Step 3: DNS check karo                            |
| cat /etc/resolv.conf                                 |
| dig +short google.com                                |
| nslookup google.com 8.8.8.8                          |
|                                                      |
| \# Step 4: Connectivity test karo                    |
| ping -c 4 gateway_ip                                 |
| ping -c 4 8.8.8.8 # Internet connectivity            |
| ping -c 4 google.com # DNS + Internet                |
|                                                      |
| \# Step 5: Port connectivity check karo              |
| nc -zv target_host 80                                |
| nc -zv target_host 443                               |
| curl -v http://target_host:8080/health               |
|                                                      |
| \# Step 6: Firewall check karo                       |
| iptables -L -n -v                                    |
| ss -tulnp \| grep &lt;port&gt;                       |

## **20.5 Service Down Troubleshooting**

| \# Step 1: Service status check karo                      |
| --------------------------------------------------------- |
| systemctl status &lt;service&gt;                          |
| journalctl -u &lt;service&gt; --since '10 minutes ago'    |
| journalctl -u &lt;service&gt; -n 50 --no-pager            |
|                                                           |
| \# Step 2: Port check karo                                |
| ss -tulnp \| grep &lt;expected_port&gt;                   |
| curl -v localhost:&lt;port&gt;/health                     |
|                                                           |
| \# Step 3: Config validate karo                           |
| nginx -t # Nginx config test                              |
| apache2ctl configtest # Apache config test                |
|                                                           |
| \# Step 4: Logs check karo                                |
| tail -100 /var/log/&lt;app&gt;/&lt;app&gt;.log            |
| tail -f /var/log/&lt;app&gt;/error.log                    |
|                                                           |
| \# Step 5: Restart karo                                   |
| systemctl restart &lt;service&gt;                         |
| systemctl status &lt;service&gt; # Verify restart success |

# **21\. Useful Aliases & Productivity Tips**

## **21.1 Recommended Bash Aliases (.bashrc mein add karo)**

| \# Navigation                                       |
| --------------------------------------------------- |
| alias ll='ls -alF --color=auto'                     |
| alias la='ls -A --color=auto'                       |
| alias l='ls -CF'                                    |
| alias ..='cd ..'                                    |
| alias ...='cd ../..'                                |
| alias ....='cd ../../..'                            |
|                                                     |
| \# Safety                                           |
| alias rm='rm -i'                                    |
| alias cp='cp -i'                                    |
| alias mv='mv -i'                                    |
|                                                     |
| \# System monitoring                                |
| alias top='htop'                                    |
| alias df='df -h'                                    |
| alias du='du -h'                                    |
| alias free='free -h'                                |
| alias ps='ps aux'                                   |
|                                                     |
| \# Networking                                       |
| alias ports='ss -tulnp'                             |
| alias myip='curl -s ifconfig.me'                    |
| alias localip='hostname -I \| awk "{print \\\$1}"'  |
|                                                     |
| \# Git shortcuts                                    |
| alias gs='git status'                               |
| alias gl='git log --oneline --graph --decorate -20' |
| alias gd='git diff'                                 |
| alias gp='git push'                                 |
|                                                     |
| \# Quick edits                                      |
| alias bashrc='nano ~/.bashrc && source ~/.bashrc'   |
| alias sshconf='nano ~/.ssh/config'                  |
|                                                     |
| \# Systemd shortcuts                                |
| alias sstart='sudo systemctl start'                 |
| alias sstop='sudo systemctl stop'                   |
| alias srestart='sudo systemctl restart'             |
| alias sstatus='sudo systemctl status'               |
| alias slogs='sudo journalctl -u'                    |

## **21.2 Keyboard Shortcuts (Bash)**

| **Command / Syntax**  | **Kya Karta Hai**                                      | **Kyu Use Karte Hain**    |
| --------------------- | ------------------------------------------------------ | ------------------------- |
| **Ctrl+R**            | History mein search karta hai                          | Previous command dhundna  |
| **Ctrl+A**            | Line ke start pe jaata hai                             | Beginning of line         |
| **Ctrl+E**            | Line ke end pe jaata hai                               | End of line               |
| **Ctrl+U**            | Cursor se line start tak delete karta hai              | Clear line start          |
| **Ctrl+K**            | Cursor se line end tak delete karta hai                | Clear line end            |
| **Ctrl+W**            | Previous word delete karta hai                         | Delete word               |
| **Alt+B**             | Ek word backward move karta hai                        | Word backward             |
| **Alt+F**             | Ek word forward move karta hai                         | Word forward              |
| **Ctrl+L**            | Screen clear karta hai (clear command jaisa)           | Clear screen              |
| **Ctrl+C**            | Running process ko SIGINT bhejta hai                   | Interrupt current command |
| **Ctrl+Z**            | Running process ko SIGTSTP bhejta hai (suspend)        | Suspend to background     |
| **Ctrl+D**            | Shell exit karta hai (EOF signal)                      | Exit shell                |
| **!!**                | Last command repeat karta hai                          | Repeat last command       |
| **!\$**               | Last command ka last argument use karta hai            | Reuse last argument       |
| **!string**           | 'string' se shuru hone wala last command run karta hai | History recall            |
| **Ctrl+P / Up Arrow** | Previous command                                       | History navigate          |

# **22\. Regular Expressions (Regex) Quick Reference**

## **22.1 Basic & Extended Regex**

| **Command / Syntax** | **Kya Karta Hai**                               | **Kyu Use Karte Hain** |
| -------------------- | ----------------------------------------------- | ---------------------- |
| **.**                | Koi bhi single character (newline ke alawa)     | Any character match    |
| **\***               | Zero ya zyada times pehle wala character repeat | Zero or more           |
| **+**                | Ek ya zyada times (ERE: -E flag ke saath grep)  | One or more            |
| **?**                | Zero ya ek baar (ERE)                           | Optional character     |
| **^**                | Line ka start                                   | Start of line anchor   |
| **\$**               | Line ka end                                     | End of line anchor     |
| **\[abc\]**          | a, b, ya c mein se koi ek                       | Character class        |
| **\[^abc\]**         | a, b, c ke alawa koi bhi character              | Negated class          |
| **\[a-z\]**          | Lowercase a se z tak koi bhi                    | Character range        |
| **\[0-9\]**          | Koi bhi digit                                   | Digit range            |
| **\\d**              | Digit (Perl regex: grep -P)                     | Any digit              |
| **\\w**              | Word character (alphanumeric + underscore)      | Word character         |
| **\\s**              | Whitespace character (space, tab)               | Whitespace match       |
| **\\b**              | Word boundary                                   | Word boundary          |
| **{n}**              | Exactly n times                                 | Exact repetition       |
| **{n,m}**            | n se m times tak                                | Range repetition       |
| **(abc)**            | Group - matching ke liye                        | Grouping               |
| **a\|b**             | a ya b (ERE)                                    | Alternation (OR)       |
| **\\1**              | Back-reference - 1st group ko match karo        | Back-reference         |

## **22.2 Common Regex Patterns (DevOps Use Cases)**

| \# IPv4 address match karo                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------ |
| grep -E '(\[0-9\]{1,3}\\.){3}\[0-9\]{1,3}' log                                                                                 |
|                                                                                                                                |
| \# Email address match karo                                                                                                    |
| grep -E '\[a-zA-Z0-9.\_%+-\]+@\[a-zA-Z0-9.-\]+\\.\[a-zA-Z\]{2,}' file                                                          |
|                                                                                                                                |
| \# URL match karo                                                                                                              |
| grep -E 'https?://\[^ \]+' file                                                                                                |
|                                                                                                                                |
| \# Timestamp match karo (2024-01-15 10:30:45)                                                                                  |
| grep -E '\[0-9\]{4}-\[0-9\]{2}-\[0-9\]{2} \[0-9\]{2}:\[0-9\]{2}:\[0-9\]{2}' log                                                |
|                                                                                                                                |
| \# HTTP status codes (4xx aur 5xx errors)                                                                                      |
| grep -E '" \[45\]\[0-9\]{2} ' access.log                                                                                       |
|                                                                                                                                |
| \# Lines jo empty nahi hain                                                                                                    |
| grep -v '^\$' file                                                                                                             |
|                                                                                                                                |
| \# Comment lines remove karo                                                                                                   |
| grep -v '^#' config.conf \| grep -v '^\$'                                                                                      |
|                                                                                                                                |
| \# Port number validate karo (1-65535)                                                                                         |
| grep -E '^(\[1-9\]\[0-9\]{0,3}\|\[1-5\]\[0-9\]{4}\|6\[0-4\]\[0-9\]{3}\|65\[0-4\]\[0-9\]{2}\|655\[0-2\]\[0-9\]\|6553\[0-5\])\$' |

# **23\. Linux Performance Tuning (SRE Level)**

## **23.1 Kernel Parameters - sysctl**

| **Command / Syntax**                    | **Kya Karta Hai**                                        | **Kyu Use Karte Hain**    |
| --------------------------------------- | -------------------------------------------------------- | ------------------------- |
| **sysctl -a**                           | Saare kernel parameters list karta hai                   | All kernel params         |
| **sysctl vm.swappiness**                | Current swappiness value dikhata hai                     | Swap aggressiveness check |
| **sysctl -w vm.swappiness=10**          | Runtime swappiness change karta hai                      | Reduce swap usage         |
| **sysctl net.core.somaxconn**           | Max socket backlog size dikhata hai                      | Connection queue size     |
| **sysctl -w net.core.somaxconn=65535**  | High-traffic servers ke liye socket backlog badhaata hai | Performance tuning        |
| **sysctl net.ipv4.tcp_max_syn_backlog** | SYN backlog size                                         | TCP SYN queue             |
| **sysctl -p /etc/sysctl.conf**          | sysctl.conf changes apply karta hai                      | Persistent param apply    |
| **sysctl vm.dirty_ratio**               | Max dirty memory percentage                              | Write caching config      |
| **sysctl fs.file-max**                  | System-wide max open files                               | File descriptor limit     |

## **23.2 ulimit - Resource Limits**

| **Command / Syntax**              | **Kya Karta Hai**                                 | **Kyu Use Karte Hain** |
| --------------------------------- | ------------------------------------------------- | ---------------------- |
| **ulimit -a**                     | Current user ke saare resource limits dikhata hai | Current limits check   |
| **ulimit -n**                     | Max open file descriptors dikhata hai             | FD limit check         |
| **ulimit -n 65536**               | Max open files 65536 set karta hai                | FD limit increase      |
| **ulimit -u**                     | Max processes dikhata hai                         | Process limit check    |
| **ulimit -m**                     | Max memory size dikhata hai                       | Memory limit check     |
| **cat /etc/security/limits.conf** | Permanent limits configuration dikhata hai        | Permanent limits file  |
| **cat /proc/sys/fs/file-max**     | System-wide max open files                        | System FD max          |
| **cat /proc/\$PID/limits**        | Specific process ke limits dikhata hai            | Process-level limits   |

## **23.3 perf - Linux Performance Analysis**

| **Command / Syntax**           | **Kya Karta Hai**                        | **Kyu Use Karte Hain** |
| ------------------------------ | ---------------------------------------- | ---------------------- |
| **perf top**                   | Real-time CPU profiling karta hai        | Hot functions identify |
| **perf record -a -g sleep 30** | 30 seconds ka profile record karta hai   | Performance recording  |
| **perf report**                | Recorded profile report dikhata hai      | Profile analysis       |
| **perf stat command**          | Command ke performance stats nikalta hai | Command profiling      |
| **perf stat -r 5 command**     | 5 runs ka average statistics             | Averaged stats         |

## **23.4 Important /proc Files**

| **Command / Syntax**  | **Kya Karta Hai**                   | **Kyu Use Karte Hain**   |
| --------------------- | ----------------------------------- | ------------------------ |
| **/proc/cpuinfo**     | CPU model, cores, frequency info    | CPU hardware details     |
| **/proc/meminfo**     | Detailed memory statistics          | Memory breakdown         |
| **/proc/loadavg**     | System load average (1, 5, 15 min)  | Load monitoring          |
| **/proc/net/tcp**     | TCP connections raw data            | Low-level connections    |
| **/proc/net/dev**     | Network interface statistics        | Network I/O stats        |
| **/proc/diskstats**   | Disk I/O statistics per device      | Disk I/O monitoring      |
| **/proc/sys/vm/**     | Memory management kernel parameters | VM tuning                |
| **/proc/sys/net/**    | Network kernel parameters           | Network tuning           |
| **/proc/PID/maps**    | Process memory map                  | Memory layout            |
| **/proc/PID/net/tcp** | Process ke TCP connections          | Per-process connections  |
| **/proc/interrupts**  | CPU interrupt counts                | Hardware interrupt stats |
| **/proc/version**     | Kernel version string               | Kernel identification    |
