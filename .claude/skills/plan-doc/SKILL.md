---
name: plan-doc
description: Use after discover-feature and before drafting. Turns the research brief into a documentation outline for the writer to approve.
---

# plan-doc

Produce a structured documentation outline from the research brief, for writer approval before any drafting begins.

## When to use this skill

Run this after `discover-feature` has produced an approved research brief. Always plan before drafting. Changing structure after a draft exists is expensive.

## Inputs

* `.claude/workspace/[TICKET-ID]/discover-feature.md`

If this file does not exist, stop and tell the writer:

> No research brief for [TICKET-ID]. Run `/discover-feature [TICKET-ID]` first.

If the brief's suggested next step is **Not ready**, stop and tell the writer which blocking questions need answers before planning.

## Steps

### Step 1: Read the research brief

Read the discover-feature brief. Identify the feature, the target audience, and what the reader will need to do after reading the documentation.

### Step 2: Determine the doc type

Use the Diataxis framework to select the appropriate doc type:

| Type | Reader need | Shape |
|---|---|---|
| **How-to guide** | Complete a specific task | Numbered steps, minimal explanation |
| **Tutorial** | Learn by doing for the first time | Guided end-to-end sequence, hand-holding tone |
| **Concept** | Understand how something works | Prose explanation, no procedures |
| **Reference** | Look up a value, parameter, or behavior | Tables, lists, terse descriptions |

Choose the type that matches what the reader will actually do with the doc. If the ticket requires more than one type, plan separate files.

### Step 3: Apply outline principles

Before writing headings, reason through these four dimensions:

**Front-load value.** The most useful information comes first. A reader scanning the top of the page should immediately understand what the doc covers and whether it applies to them. Background follows actionable content. It does not precede it.

**Optimize for scanning.** Readers rarely read linearly. Each heading should clearly signal the content beneath it. Avoid vague headings like "Overview" or "More information."

**Separate concept from procedure.** Do not mix explanation and steps in the same section. If readers need to understand something before they can do something, that understanding belongs in its own section, not embedded inside a procedure.

**Identify prerequisites.** What must the reader already know or have set up before this doc is useful? This belongs near the top.

### Step 4: Determine the file path

Find the documentation folder under "Repository structure" in the project instruction file. If it is not listed, ask the writer.

Based on the doc type and subject matter, identify where the file belongs in that folder. Use existing files in the same area as a guide for naming conventions. If this is an update to an existing file, note that instead.

### Step 5: Write the plan

Write `.claude/workspace/[TICKET-ID]/plan.md` using this structure:

```markdown
# Plan: [TICKET-ID]

## Doc type
[Type]: [One sentence explaining why this type fits the reader need]

## File
* Path: [documentation folder]/[path/to/file.md]
* Status: New file | Update to existing file

## Front matter
title: [Proposed title]
description: [One sentence describing what the reader will learn or accomplish]

## Prerequisite knowledge
[What the reader must already know. If none, say so.]

## Outline

### [Section heading]
Purpose: [What this section does for the reader, in one sentence]
Content: [Key points, decisions, or data this section must cover]

### [Section heading]
Purpose: ...
Content: ...

## Open questions
The brief's open questions, as one list. For each, name the sections it affects.
Do not write GAP or VERIFY markers here. `draft-doc` places them.

## Decisions for the writer
Choices the sources do not settle, which the writer makes before drafting.
For each one, give the options and recommend one.

For example:
* **Where to add the new sections.** A: after section 8, renumbering the sections
  after it. B: at the end, with no renumbering. Recommended: A, so related
  sections stay together.
```

## Output

`.claude/workspace/[TICKET-ID]/plan.md`

## Transition

After writing the plan, show the headings and purpose of each section, list the decisions for the writer, and say:

> "Approve the plan or tell me what to change, then run `/draft-doc [TICKET-ID]`."

**Stop here and wait for the writer's response before taking any further action.**

## Rules

* Do not start drafting until the plan is approved.
* If a section depends on an open question, write "See open question [N]" in its Content line. Do not invent content to fill it.
* Choose the doc type based on reader need, not on what is easiest to write.
