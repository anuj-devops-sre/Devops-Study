# Git — Zero to Mid-Level Reference

A practical, command-first guide. Each section builds on the previous one. Run the commands as you read.

---

## Table of Contents

1. [What Git Actually Is](#1-what-git-actually-is)
2. [Installation & First-Time Setup](#2-installation--first-time-setup)
3. [The Three Areas (Mental Model)](#3-the-three-areas-mental-model)
4. [Starting a Repo](#4-starting-a-repo)
5. [The Daily Loop: status → add → commit](#5-the-daily-loop-status--add--commit)
6. [Looking at History](#6-looking-at-history)
7. [Ignoring Files](#7-ignoring-files)
8. [Branching](#8-branching)
9. [Merging](#9-merging)
10. [Remotes: push, pull, fetch](#10-remotes-push-pull-fetch)
11. [Undoing Things](#11-undoing-things)
12. [Stash — Park Work Temporarily](#12-stash--park-work-temporarily)
13. [Rebase vs Merge](#13-rebase-vs-merge)
14. [Interactive Rebase & Squashing](#14-interactive-rebase--squashing)
15. [Cherry-Pick](#15-cherry-pick)
16. [Tags](#16-tags)
17. [Resolving Merge Conflicts](#17-resolving-merge-conflicts)
18. [Reflog — Your Safety Net](#18-reflog--your-safety-net)
19. [Common Workflows](#19-common-workflows)
20. [Cheatsheet](#20-cheatsheet)

---

## 1. What Git Actually Is

Git is a **distributed version control system**. Every clone is a full repository with complete history — not just a checkout from a central server. That's why most operations are local and instant.

Key idea: Git stores **snapshots**, not diffs. Each commit is a pointer to a complete tree of files. Identical files across commits are stored once (deduplicated by SHA-1 hash).

**Vocabulary you'll hit constantly:**
- **Repository (repo)** — the `.git/` folder plus your files
- **Commit** — a snapshot + metadata (author, message, parent commit)
- **Branch** — a movable pointer to a commit
- **HEAD** — pointer to the commit you currently have checked out
- **Remote** — another copy of the repo, usually on a server (GitHub, GitLab, Bitbucket)
- **Origin** — default name for the remote you cloned from

---

## 2. Installation & First-Time Setup

**Install:**
- macOS: `brew install git`
- Ubuntu/Debian: `sudo apt install git`
- Windows: download from git-scm.com

**Verify:**
```bash
git --version
```

**One-time config (do this once per machine):**
```bash
git config --global user.name "Anuj Dwivedi"
git config --global user.email "anuj.dwivedi@cashify.in"
git config --global init.defaultBranch main
git config --global pull.rebase false   # use merge on pull (safer default)
git config --global core.editor "vim"   # or nano, code --wait, etc.
```

**View config:**
```bash
git config --list
git config --global --edit   # opens ~/.gitconfig
```

**Set up SSH for GitHub/GitLab** (recommended over HTTPS):
```bash
ssh-keygen -t ed25519 -C "anuj.dwivedi@cashify.in"
cat ~/.ssh/id_ed25519.pub   # paste into GitHub → Settings → SSH Keys
ssh -T git@github.com       # verify
```

---

## 3. The Three Areas (Mental Model)

```
┌────────────────┐   git add    ┌──────────────┐   git commit   ┌──────────────┐
│ Working Dir    │ ───────────▶ │ Staging Area │ ─────────────▶ │ Repository   │
│ (your files)   │              │ (index)      │                │ (.git/)      │
└────────────────┘              └──────────────┘                └──────────────┘
        ▲                                                              │
        └──────────────────── git checkout / restore ──────────────────┘
```

- **Working Directory** — files you're editing right now
- **Staging Area (Index)** — what will go into the next commit
- **Repository** — committed history

This three-stage model is why you can selectively commit parts of your changes.

---

## 4. Starting a Repo

**Option A — new project from scratch:**
```bash
mkdir my-project && cd my-project
git init
```

**Option B — clone an existing repo:**
```bash
git clone git@github.com:reglobe/some-repo.git
git clone https://github.com/reglobe/some-repo.git
git clone <url> custom-folder-name
```

**Option C — start from an existing folder and connect to a remote:**
```bash
cd existing-folder
git init
git remote add origin git@github.com:reglobe/new-repo.git
git add .
git commit -m "Initial commit"
git push -u origin main
```

---

## 5. The Daily Loop: status → add → commit

```bash
git status                    # what's changed, what's staged
git add file.txt              # stage one file
git add src/                  # stage a directory
git add .                     # stage everything in current dir
git add -p                    # stage interactively (hunk by hunk) — very useful
git commit -m "Fix login bug"
git commit                    # opens editor for longer message
git commit -am "msg"          # stage + commit tracked files (skips untracked)
```

**Good commit messages:**
```
Short summary (50 chars or less, imperative mood)

Longer explanation if needed. Wrap at 72 chars. Explain *why*,
not *what* — the diff already shows what changed.

Refs: INFOSEC-1234
```

**Amend the last commit** (forgot a file or typo in message):
```bash
git add forgotten-file.txt
git commit --amend                    # opens editor
git commit --amend -m "New message"
git commit --amend --no-edit          # keep message, just add staged files
```

⚠️ Don't amend commits you've already pushed to a shared branch.

---

## 6. Looking at History

```bash
git log                              # full history
git log --oneline                    # one commit per line
git log --oneline --graph --all      # visual branch graph
git log -5                           # last 5 commits
git log --author="Anuj"
git log --since="2 weeks ago"
git log -- path/to/file              # history of one file
git log -p file                      # history WITH diffs
git show <commit-hash>               # details of one commit
git show HEAD                        # last commit
git show HEAD~3                      # 3 commits before HEAD
```

**See what changed:**
```bash
git diff                  # unstaged changes
git diff --staged         # staged changes (what's going into next commit)
git diff main feature     # difference between two branches
git diff HEAD~3 HEAD      # last 3 commits worth of changes
```

---

## 7. Ignoring Files

Create a `.gitignore` in the repo root:

```gitignore
# Dependencies
node_modules/
__pycache__/
*.pyc
venv/

# Build artifacts
dist/
build/
*.log

# Env / secrets
.env
.env.local
*.pem
*.key

# IDE
.vscode/
.idea/
.DS_Store
```

If a file is already tracked, `.gitignore` won't untrack it. Use:
```bash
git rm --cached secrets.env    # stop tracking but keep file on disk
```

**Tip:** use [gitignore.io](https://www.toptal.com/developers/gitignore) to generate templates per language/framework.

---

## 8. Branching

```bash
git branch                      # list local branches
git branch -a                   # list all (including remote)
git branch feature/new-login    # create branch
git switch feature/new-login    # switch to it (modern syntax)
git switch -c feature/new-login # create + switch in one step
git checkout feature/new-login  # older syntax, same effect
git checkout -b feature/new-login

git branch -d old-branch        # delete (safe — refuses if unmerged)
git branch -D old-branch        # force delete
git branch -m old-name new-name # rename
```

**Branch naming convention** (typical):
- `feature/short-description`
- `bugfix/INFOSEC-1234-fix-xss`
- `hotfix/critical-payment-bug`
- `release/v2.4.0`

---

## 9. Merging

Bring changes from another branch into your current one:

```bash
git switch main
git merge feature/new-login
```

Three things can happen:

1. **Fast-forward** — main hasn't moved since branch was created. Git just moves the pointer forward. No merge commit.
2. **Three-way merge** — both branches have new commits. Git creates a merge commit combining them.
3. **Conflict** — same lines changed differently in both branches. You must resolve manually (see Section 17).

**Force a merge commit even if fast-forward is possible** (preserves the fact that work happened on a branch):
```bash
git merge --no-ff feature/new-login
```

---

## 10. Remotes: push, pull, fetch

```bash
git remote -v                              # list remotes with URLs
git remote add origin <url>                # add a remote
git remote set-url origin <new-url>        # change URL
git remote remove origin

git push                                   # push current branch
git push -u origin feature/new-login       # first push (sets upstream tracking)
git push origin --delete old-branch        # delete remote branch

git fetch                                  # download remote changes, don't merge
git pull                                   # = fetch + merge
git pull --rebase                          # = fetch + rebase (cleaner history)
```

**`fetch` vs `pull`** — `fetch` is read-only; it just updates your knowledge of the remote. `pull` actually changes your working branch. When in doubt, `fetch` first, inspect with `git log origin/main`, then merge or rebase consciously.

---

## 11. Undoing Things

This is where most beginners panic. Stay calm — Git almost never truly loses work (see reflog).

**Unstage a file** (was `git add`ed by mistake):
```bash
git restore --staged file.txt        # modern
git reset HEAD file.txt              # older syntax
```

**Discard unstaged changes** (⚠️ irreversible for uncommitted changes):
```bash
git restore file.txt                 # discard changes to one file
git restore .                        # discard all unstaged changes
git checkout -- file.txt             # older syntax
```

**Undo the last commit but keep changes:**
```bash
git reset --soft HEAD~1     # uncommit, keep changes staged
git reset --mixed HEAD~1    # uncommit, keep changes unstaged (default)
git reset --hard HEAD~1     # ⚠️ uncommit AND delete changes
```

**Revert a commit** (creates a new commit that undoes it — safe for pushed commits):
```bash
git revert <commit-hash>
git revert HEAD             # revert most recent commit
```

**Reset modes summary:**

| Mode    | HEAD moves | Staging area | Working dir |
|---------|------------|--------------|-------------|
| --soft  | ✓          | unchanged    | unchanged   |
| --mixed | ✓          | reset        | unchanged   |
| --hard  | ✓          | reset        | reset ⚠️    |

---

## 12. Stash — Park Work Temporarily

You're mid-feature, someone needs a hotfix on main. You don't want to commit half-done work.

```bash
git stash                       # save changes, clean working dir
git stash push -m "WIP login"   # with a message
git stash -u                    # include untracked files
git stash list                  # see all stashes
git stash show -p stash@{0}     # view changes in a stash
git stash pop                   # apply latest stash AND remove it
git stash apply stash@{1}       # apply a specific stash, keep it
git stash drop stash@{0}        # delete a stash
git stash clear                 # delete all stashes
```

---

## 13. Rebase vs Merge

Both integrate changes from one branch into another. They produce different history shapes.

**Merge** preserves the actual timeline. Branches stay visible as branches.
```
A---B---C---M (main)
     \     /
      D---E (feature)
```

**Rebase** rewrites your feature commits to look like they started from the tip of main. Linear history.
```
A---B---C---D'---E' (feature, after rebase)
```

```bash
git switch feature
git rebase main
```

If conflicts: resolve them → `git add <files>` → `git rebase --continue`. To bail out: `git rebase --abort`.

**Golden rule:** never rebase commits that have been pushed to a shared branch. You're rewriting history; everyone else's clones will break. Rebase local work; merge shared work.

---

## 14. Interactive Rebase & Squashing

Clean up commits before opening a PR. Suppose your branch has 6 messy commits:

```bash
git rebase -i HEAD~6
```

Editor opens with:
```
pick a1b2c3d Add login form
pick e4f5g6h Fix typo
pick i7j8k9l Fix another typo
pick m1n2o3p Add validation
pick q4r5s6t WIP
pick u7v8w9x Address review
```

Change `pick` to:
- `reword` (`r`) — keep commit, edit message
- `squash` (`s`) — combine into previous commit, merge messages
- `fixup` (`f`) — like squash but discard this commit's message
- `drop` (`d`) — delete the commit
- `edit` (`e`) — pause to amend the commit

Reorder lines to reorder commits. Save & close to apply.

**Common pattern — squash everything into one clean commit:**
```
pick a1b2c3d Add login form
fixup e4f5g6h Fix typo
fixup i7j8k9l Fix another typo
fixup m1n2o3p Add validation
fixup q4r5s6t WIP
fixup u7v8w9x Address review
```

After rebase, force-push your branch (since history changed):
```bash
git push --force-with-lease     # safer than --force
```

`--force-with-lease` refuses to push if someone else pushed to the branch since you last fetched. Always prefer it over `--force`.

---

## 15. Cherry-Pick

Apply a single commit from another branch onto your current one:

```bash
git cherry-pick <commit-hash>
git cherry-pick a1b2c3d e4f5g6h         # multiple
git cherry-pick A..B                    # range (exclusive of A)
git cherry-pick --no-commit <hash>      # apply changes but don't commit yet
```

Useful for backporting a hotfix from `main` to a `release/v1.x` branch.

---

## 16. Tags

Tags are immutable pointers to specific commits — typically used for releases.

```bash
git tag                                    # list tags
git tag v1.0.0                             # lightweight tag (just a label)
git tag -a v1.0.0 -m "Release 1.0.0"       # annotated tag (recommended)
git tag -a v1.0.0 <commit-hash>            # tag a specific past commit
git show v1.0.0
git push origin v1.0.0                     # push one tag
git push origin --tags                     # push all tags
git tag -d v1.0.0                          # delete local tag
git push origin --delete v1.0.0            # delete remote tag
```

Use [semantic versioning](https://semver.org): `vMAJOR.MINOR.PATCH`.

---

## 17. Resolving Merge Conflicts

When Git can't auto-merge, it marks the conflict in the file:

```
<<<<<<< HEAD
const timeout = 5000;
=======
const timeout = 10000;
>>>>>>> feature/new-login
```

**Resolve:**
1. Open the file. Decide what the final content should be.
2. Delete the `<<<<<<<`, `=======`, `>>>>>>>` markers.
3. Save.
4. `git add <file>` to mark as resolved.
5. `git commit` (for merge) or `git rebase --continue` (for rebase).

**Helpful commands during a conflict:**
```bash
git status                  # shows conflicted files
git diff                    # shows conflict markers
git checkout --ours file    # keep our version entirely
git checkout --theirs file  # keep their version entirely
git merge --abort           # bail out of the merge
git rebase --abort          # bail out of the rebase
```

**Use a merge tool:**
```bash
git mergetool               # opens configured tool (vimdiff, meld, vscode, etc.)
```

---

## 18. Reflog — Your Safety Net

Reflog records every move HEAD makes locally. If you ever think you've "lost" commits (after a bad reset, rebase, or branch delete), reflog has them.

```bash
git reflog
```

Output:
```
a1b2c3d HEAD@{0}: reset: moving to HEAD~3
e4f5g6h HEAD@{1}: commit: Add login form
i7j8k9l HEAD@{2}: checkout: moving from main to feature
```

**Recover:**
```bash
git reset --hard HEAD@{1}        # go back to before the bad reset
git checkout -b recovered e4f5g6h # create a branch from a lost commit
```

Reflog entries expire after ~90 days by default. Until then, very little is truly lost.

---

## 19. Common Workflows

### Feature Branch Workflow (most common)
```bash
git switch main
git pull
git switch -c feature/new-thing
# ... work, commit, commit ...
git push -u origin feature/new-thing
# Open Pull Request on GitHub/GitLab
# After review + merge:
git switch main
git pull
git branch -d feature/new-thing
```

### Keeping a long-running branch up to date
```bash
git switch feature/big-thing
git fetch origin
git rebase origin/main           # or: git merge origin/main
# resolve any conflicts
git push --force-with-lease       # if you rebased
```

### Hotfix on production
```bash
git switch main
git pull
git switch -c hotfix/payment-bug
# ... fix, commit ...
git push -u origin hotfix/payment-bug
# PR → merge → tag a release
git tag -a v2.4.1 -m "Hotfix payment bug"
git push origin v2.4.1
```

---

## 20. Cheatsheet

| Task                            | Command                                  |
|---------------------------------|------------------------------------------|
| Initialize repo                 | `git init`                               |
| Clone repo                      | `git clone <url>`                        |
| Check status                    | `git status`                             |
| Stage file                      | `git add <file>`                         |
| Stage interactively             | `git add -p`                             |
| Commit                          | `git commit -m "msg"`                    |
| Amend last commit               | `git commit --amend`                     |
| View history                    | `git log --oneline --graph --all`        |
| Show changes (unstaged)         | `git diff`                               |
| Show changes (staged)           | `git diff --staged`                      |
| Create + switch branch          | `git switch -c <branch>`                 |
| List branches                   | `git branch -a`                          |
| Delete branch                   | `git branch -d <branch>`                 |
| Merge branch                    | `git merge <branch>`                     |
| Rebase onto branch              | `git rebase <branch>`                    |
| Interactive rebase              | `git rebase -i HEAD~N`                   |
| Push                            | `git push`                               |
| Push new branch                 | `git push -u origin <branch>`            |
| Pull                            | `git pull`                               |
| Fetch only                      | `git fetch`                              |
| Stash changes                   | `git stash`                              |
| Apply stash                     | `git stash pop`                          |
| Cherry-pick                     | `git cherry-pick <hash>`                 |
| Create tag                      | `git tag -a v1.0 -m "msg"`               |
| Push tags                       | `git push origin --tags`                 |
| Discard local changes           | `git restore <file>`                     |
| Unstage file                    | `git restore --staged <file>`            |
| Undo last commit (keep changes) | `git reset --soft HEAD~1`                |
| Revert a commit safely          | `git revert <hash>`                      |
| Recover lost commit             | `git reflog` → `git reset --hard <ref>`  |
| Force push safely               | `git push --force-with-lease`            |

---

## Further Reading

- **Pro Git book** (free): https://git-scm.com/book
- **Oh Shit, Git!?!**: https://ohshitgit.com — recovery recipes for common mistakes
- **Learn Git Branching** (interactive): https://learngitbranching.js.org
- **git-scm cheat sheet**: https://training.github.com/downloads/github-git-cheat-sheet.pdf

---

*The fastest way to get fluent: use Git daily for a real project. Read `git help <command>` whenever you're unsure — Git's man pages are excellent.*
