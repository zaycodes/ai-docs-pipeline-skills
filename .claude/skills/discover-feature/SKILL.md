---
name: discover-feature
description: Use before planning or drafting a doc. Researches a ticket, or ticket content you paste in, and writes a research brief with confirmed facts, open questions, and a suggested next step.
---

# discover-feature

Research a ticket and produce a structured research brief before any writing begins.

## When to use this skill

Run this before planning or drafting any documentation. `plan-doc` and `draft-doc` both read the research brief this skill produces, so they only work once this has run.

Use it any time you need to document a feature or change that you did not build yourself and are not yet fully familiar with.

## Inputs

One of:

* **A ticket ID or URL**, for example `DOC-1234`. Fetch the ticket in Step 3.
* **The ticket content**, pasted into the chat or as a path to a file. Use it as the ticket in Step 3. If it has no ticket ID, ask the writer for a short ID to name the workspace folder, for example `archive-endpoints`.

## Steps

### Step 1: Parse the ticket ID

Extract the ticket ID from whatever the writer provided: a URL, a plain ID, or a mention. Use the full ID as-is.

### Step 2: Create the workspace directory

Create `.claude/workspace/[TICKET-ID]/`. This directory holds all working files for this ticket and is scoped to the feature branch. It never merges to main.

### Step 3: Fetch the ticket

If the writer gave you the ticket content, use it and skip fetching.

Otherwise, use your issue tracker integration to fetch the ticket. In order of preference: an MCP server for your tracker (Jira, Linear, GitHub Issues, and others all have one), a built-in integration or command-line tool your AI coding agent can use for that tracker, or, if neither exists, ask the writer to paste the ticket content into the chat. Collect:

* Title and description
* Acceptance criteria
* Any linked tickets
* Any linked documentation pages (fetch each one)
* Any file attachments: read text-based files directly and note binary files you cannot read

For each attachment you cannot read, note the filename and type in the brief under "Unread attachments."

### Step 4: Search the knowledge base

Search your internal knowledge base for context related to this feature. Use the ticket title and key terms as your search query. This could be Confluence, Notion, a search tool like Glean, or any internal wiki your team uses. Look for:

* Engineering documentation or design specs
* Product specs
* Related feature context that fills gaps in the ticket

If no knowledge base is connected, skip this step and say so under Sources.

### Step 5: Find related existing documentation

Search the documentation folder listed under "Repository structure" in the project instruction file for existing documentation related to this feature. Note the file paths of any docs that may need to be updated or cross-linked.

### Step 6: Write the research brief

Write `.claude/workspace/[TICKET-ID]/discover-feature.md` using this structure:

```markdown
# [TICKET-ID]: [Ticket title]

## What this feature does
Plain-language explanation. What it is, what problem it solves, what a user
can do with it that they could not do before.

## What's changing
Only changes the sources confirm. Unconfirmed statements go in Open questions.
* New: [what was added]
* Changed: [what was modified and how it differs from before]
* Removed: [what no longer exists]

## Target audience
Who uses this feature. Their technical level, role, and goal.

## Existing docs
List of related files with paths. Note whether each needs to be updated or cross-linked.

## Confirmed facts
The specifics the doc will rely on, such as permissions, defaults, limits, and
responses. Give the source for each one.

## Open questions
Format each as a specific, answerable question.

### Blocking
Questions the doc cannot be written correctly without, or whose answer would change
the doc type or structure. These go to the SME before drafting.

### Non-blocking
Questions the draft can carry as a VERIFY or GAP marker.

## Suggested next step
One of:
* **Ready to plan.** No blocking questions.
* **Plan now, answer before drafting.** Blocking questions exist, but none change the
  doc type or structure. Send them to [SME] while planning goes ahead.
* **Not ready.** The sources are too thin, or a blocking question changes the doc type
  or structure. Get answers first.

## Sources
Ticket URL, pages read, attachments read, knowledge base results used.

## Unread attachments
[Omit this section if all attachments were read successfully.]
```

## Output

`.claude/workspace/[TICKET-ID]/discover-feature.md`

## Transition

After writing the brief, summarize it in 3 to 5 sentences, state the suggested next step, and say:

> "Read the brief, then run `/plan-doc [TICKET-ID]` when you're ready."

**Stop here and wait for the writer's response before taking any further action.**

## Rules

* Only include information stated or directly supported by the source material.
* Do not invent product behavior. If something is unclear, put it in Open questions.
* If information is implied but not stated, note it in Open questions, not in the main sections.
* Terminology inconsistency is a factual error. Note exact phrasing from sources and use it consistently.
