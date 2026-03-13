---
name: commit-local
description: Commit all outstanding work locally (no push) with a descriptive commit message
argument-hint: [optional commit message]
---

# Commit Local Skill

Stage and commit all outstanding changes locally without pushing. Generates a descriptive commit message based on the actual changes.

## Usage

```
/commit-local                     # auto-generate commit message from changes
/commit-local fix dataset typos   # use provided message as basis
```

## Workflow

### Step 1: Assess the Working Tree

Run `git status` and `git diff --stat` to understand what's changed. If there are no changes (clean working tree), report that and stop.

### Step 2: Understand the Changes

- For modified files: review the diff to understand what changed
- For new files: read the first ~30 lines to understand their purpose
- For deleted files: note what was removed

### Step 3: Stage Files

Stage all modified and untracked files relevant to the work. Use specific file paths (not `git add -A`). Do NOT stage:
- `.env` or files containing secrets/credentials
- Large binary files unless clearly intentional
- Files in `.gitignore`

### Step 4: Write the Commit Message

If the user provided a message argument, use it as the basis but expand it into a proper commit message.

If no message was provided, generate one:
- First line: concise summary of what changed (imperative mood, under 72 chars)
- Blank line
- Body: bullet points describing the key changes (what and why, not how)
- End with the co-author line

Follow the repository's existing commit style (check `git log --oneline -5`).

### Step 5: Commit

Create the commit using a HEREDOC format. Always include:

```
Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

### Step 6: Verify and Report

Run `git status` to confirm the commit succeeded and the tree is clean. Report the short SHA and summary.

### Step 7: Notify

Send a Pushover notification with a concise message about what was committed.

## Important

- **Never push.** This skill only commits locally.
- **Never amend.** Always create a new commit.
- **Never use `--no-verify`.** If pre-commit hooks fail, fix the issue and retry.
