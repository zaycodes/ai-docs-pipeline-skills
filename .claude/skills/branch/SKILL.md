---
name: branch
description: Use as the first step on a documentation ticket. Creates a correctly named git branch from the ticket ID.
---

# branch

Create a correctly named git branch from a ticket before starting any documentation work.

## When to use this skill

Run this as the first step when starting work on any ticket. It ensures branch names are consistent, traceable to the ticket, and do not require the writer to manually construct the slug.

## Inputs

* Ticket ID: the full ticket identifier, for example `DOC-1234` or `ISSUE-567`

## Steps

### Step 1: Check the current branch

Find the repository's default branch:

```bash
git symbolic-ref --short refs/remotes/origin/HEAD
```

The output is `origin/` followed by the default branch, for example `origin/main`. If the command fails, use `main` if that branch exists, otherwise `master`.

Run `git branch --show-current`. If the current branch is not the default branch, stop and tell the writer:

> Cannot create branch: you are currently on `[branch-name]`, not `[default-branch]`. Switch to `[default-branch]` first.

Do not proceed until the writer is on the default branch.

### Step 2: Fetch the ticket title

Use your issue tracker integration to fetch the ticket and read its title or summary field. The field name varies by tool: `summary` in Jira, `title` in GitHub Issues and Linear.

"Issue tracker integration" means one of, in order of preference: an MCP server for your tracker (Jira, Linear, GitHub Issues, and others all have one), a built-in integration your AI coding agent already has for that tracker, or, if neither exists, the writer pastes the ticket title directly into the chat instead of this step fetching it automatically.

### Step 3: Derive the branch name slug

Transform the ticket title into a short, URL-safe slug:

* Lowercase every letter
* Keep the first five words of the title
* Replace spaces with hyphens
* Remove parentheses, commas, and periods
* Replace any remaining special characters (except letters, digits, and hyphens) with hyphens
* Collapse consecutive hyphens into one

Keep the ticket ID exactly as it is in the tracker. Only the title part is lowercased.

Examples:

| Ticket | Title | Branch name |
|---|---|---|
| DOC-1234 | Release notes (June 3, 2024) | `DOC-1234-release-notes-june-3-2024` |
| DOC-102 | Document the new task archive endpoints | `DOC-102-document-the-new-task-archive` |

### Step 4: Create the branch

```bash
git checkout -b [TICKET-ID]-[TITLE-SLUG]
```

Confirm the branch was created and report the full branch name to the writer.

## Output

A new local git branch named `[TICKET-ID]-[TITLE-SLUG]`.

## Rules

* Never create a branch from anything other than the default branch.
* Never modify the ticket title when deriving the slug. Only apply the transformations in Step 3.
