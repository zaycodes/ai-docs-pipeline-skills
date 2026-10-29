---
name: draft-doc
description: Use after plan-doc, once the plan is approved. Writes the draft from the plan and brief, flagging gaps and unverified content inline.
---

# draft-doc

Write the documentation draft from the approved plan and research brief.

## When to use this skill

Run this after `plan-doc` has produced a plan that the writer has approved. Do not draft without an approved plan.

## Inputs

* `.claude/workspace/[TICKET-ID]/plan.md`
* `.claude/workspace/[TICKET-ID]/discover-feature.md`

If either file is missing, stop and tell the writer which one, and which skill creates it:

> No plan for [TICKET-ID]. Run `/plan-doc [TICKET-ID]` first.

> No research brief for [TICKET-ID]. Run `/discover-feature [TICKET-ID]` first.

## Steps

### Step 1: Extract verified content from sources

Before writing anything, scan both input files and identify:

* Key terms and their exact phrasing. Use these verbatim throughout the draft. Terminology inconsistency is a factual error.
* Specific values, settings, and defaults that are explicitly stated.
* Behaviors that are directly described vs. behaviors that are implied.

### Step 2: Draft section by section

Follow the section order from `plan.md` exactly. Apply the writer's answers to "Decisions for the writer" in the plan. If a decision has no answer, use the recommendation and say so when you report back.

For each section:

1. Re-read the section's Purpose and Content notes from the plan.
1. Identify which source material from the research brief covers that content.
1. Write the section using only that material.
1. Insert gap or verify markers wherever the sources fall short (see Markers below).

Do not skip sections. A section with only a gap marker is more honest than a section with invented content.

### Step 3: Apply writing standards

* Lead with what the reader will do or understand. Do not lead with how the feature works internally.
* Do not restate what a UI label already says. Document what the reader needs to decide or understand, not what they can see.
* Do not use generic filler introductions ("This document describes how to...").
* Procedures longer than seven steps need an intermediate checkpoint or verification step.
* Every sentence begins with the information it contains, not a preamble announcing that information is coming.

### Step 4: Write the draft file

Write the draft to the path specified in `plan.md` under File > Path. Use the front matter from the plan as the starting point.

Also save a copy to `.claude/workspace/[TICKET-ID]/draft.md` as a working snapshot.

## Failure modes

AI drafts go wrong in the same ways. Check the draft for each one before you finish.

* **Generic introduction.** An opening that restates the title or announces the page ("This page describes how to..."). Start with what the reader does or gets.
* **Unrequested FAQ.** An FAQ or "Common questions" section the plan did not ask for. If a question matters, answer it where the reader needs it.
* **Implementation before intent.** Explaining how the feature works inside before saying what the reader uses it for.
* **Concept content in a task or reference page.** Background explanation added to a how-to guide or reference page. Link to a concept page instead.
* **Half-updated page.** Changing one part of the page but not another part that says the same thing, for example a permissions table and an endpoints table.

## Markers

Use these inline markers to flag content that needs writer attention. They render as HTML comments: visible in the source, invisible when the site builds.

**Gap:** information the plan calls for that is not in the sources:
```
<!-- GAP: [describe what's missing and where to find it] -->
```

**Verify:** content that is inferred rather than directly stated in a source:
```
<!-- VERIFY: [describe the assumption and which source it is based on] -->
```

Insert markers at the exact location where missing or uncertain content belongs. Do not consolidate them at the bottom of the file.

## Output

* Draft written to the path in `plan.md`
* Working copy at `.claude/workspace/[TICKET-ID]/draft.md`

## After drafting

Count the gap and verify markers and report them to the writer:

* How many `<!-- GAP -->` markers exist and what they represent
* How many `<!-- VERIFY -->` markers exist and what assumptions they contain

Then say: "The draft is at `[file path]`. Read it and resolve the markers you can, then run `/doc-review [TICKET-ID]`."

## Rules

* Only write what the sources in the research brief support.
* Do not invent product behavior, API parameters, default values, or UI labels.
* Do not skip sections from the plan. A missing section is always visible.
* Use exact terminology from the research brief throughout. Do not paraphrase technical terms.
