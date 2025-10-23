# Git command overview
## Basics
```bash
git init                     # Create a new Git repository
git clone <url>              # Clone an existing repo
git status                   # Show changed files and branch info
git add .                    # Stage all changes
git commit -m "message"      # Commit staged changes
git push                     # Push commits to remote
git pull                     # Fetch + merge latest remote changes
```

## Branching and merging
```bash
git branch                   # List branches
git branch <name>            # Create new branch
git checkout <name>          # Switch to branch
git checkout -b <name>       # Create and switch to branch
git merge <branch>           # Merge another branch into current
git branch -d <name>         # Delete a branch
git branch -D <name>         # Force delete a branch
git push origin <branch>     # Push branch to remote
git push origin --delete <branch>  # Delete remote branch
```

## Undo & Fix
```bash
git restore <file>           # Discard local changes to a file
git restore --staged <file>  # Unstage a file
git reset HEAD <file>        # Unstage a file (alternative)
git reset --hard HEAD        # Reset everything to last commit
git reset --soft HEAD~1      # Undo last commit but keep changes staged
git revert <commit>          # Make a new commit that undoes a commit
git stash                    # Temporarily store uncommitted changes
git stash list               # List stored stashes
git stash pop                # Reapply and remove last stash
git stash apply stash@{n}    # Reapply specific stash
```

## History and info
```bash
git log                      # Show commit history
git log --oneline --graph    # Compact visual history
git show <commit>            # Show details of a specific commit
git diff                     # Show unstaged changes
git diff --staged            # Show staged changes
git blame <file>             # Show who changed each line last
git reflog                   # Show all repo actions, even deleted commits
```

## Remote repositories
```bash
git remote -v                # Show remote URLs
git remote add origin <url>  # Add a remote repository
git remote remove origin     # Remove a remote
git fetch origin             # Fetch changes without merging
git pull origin <branch>     # Pull latest changes from a branch
git push -u origin <branch>  # Push and set upstream tracking
git remote show origin       # Show detailed info about remotes
```

## Tags and versions
```bash
git tag                      # List all tags
git tag <name>               # Create a lightweight tag
git tag -a v1.0 -m "msg"     # Create an annotated tag
git push origin v1.0         # Push a specific tag
git push origin --tags       # Push all tags
```

## Cleaning and search
```bash
git clean -fd                # Remove untracked files and directories
git grep "keyword"           # Search for text in tracked files
git shortlog -sn             # Show commit count by author
git describe --tags           # Show nearest tag for current commit
```

## Configuration
```bash
git config --list             # Show current Git settings
git config user.name "Your Name"
git config user.email "you@example.com"
git config core.autocrlf true # Handle line endings (Windows)
git config core.autocrlf input # Use LF only (Linux/macOS)
git help <command>            # Show Git manual for a specific command
```

## Git advanced commands
```bash
git cherry-pick <commit>      # Apply a specific commit to current branch
git rebase <branch>           # Replay commits onto another branch
git rebase -i HEAD~3          # Interactive rebase to edit, squash, reorder
git bisect start              # Start binary search to find a bad commit
git bisect good/bad           # Mark commits during bisecting
git reflog                    # Show history of all changes, even removed
git mv <old> <new>            # Rename/move a file
git rm <file>                 # Remove file from repo and disk
git show-branch               # Show branches and their commits
```