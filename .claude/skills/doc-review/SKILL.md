---
name: doc-review
description: Use on a draft before publishing. Takes a ticket ID to review that ticket's draft, or a file path to review any page. Runs the lint script, then a qualitative review and a cold-reader check.
---

# doc-review

Perform a strict editorial review of a documentation file before publishing.

## When to use this skill

Run this on any draft before it is published, whether AI-generated or human-written. Use it as a final pass before requesting peer review, or after incorporating feedback to verify all issues are resolved.

## Inputs

The writer gives you either a ticket ID or a file path.

### A ticket ID, for example `DOC-1234`

Use this when the page went through the pipeline.

1. Open `.claude/workspace/[TICKET-ID]/plan.md`.
1. Find the page's path under **File > Path**. This is the page `draft-doc` wrote.
1. Review that page.

If `plan.md` is missing, or the page it names does not exist, stop and tell the writer:

> No draft to review for [TICKET-ID]. Run `plan-doc` and `draft-doc` first.

### A file path, for example `docs/api/tasks.md`

Use this to review any page, including pages that did not go through the pipeline. Review the file directly. You do not need a plan or a workspace folder.

## Steps

### Step 1: Run the lint script

Run the lint script on the file. Do not skip this step.

```bash
python .claude/skills/doc-review/scripts/lint.py <file-path>
```

If the script is missing, stop and tell the writer to add it from the skills repo.

The script catches mechanical issues that do not need judgment. Read its output and sort each finding:

* **Keep** findings in content this ticket added or changed. In ticket mode, run `git diff [default-branch] -- <file-path>` to see which lines changed. Find the default branch the same way `branch` does. With a file path, keep every finding.
* **Move to Pre-existing** findings in content the ticket did not touch.
* **Dismiss** false positives, with a one-line reason. For example, a passive sentence where the actor is unknown, or text the project instruction file says to keep as it is.

### Step 2: Qualitative review

Read the full document and evaluate each dimension below. Flag genuine problems only. Do not flag hypothetical ones.

**Concision**
Flag sentences that use more words than necessary. Setup phrases, hedging language, and redundant qualifiers are the most common culprits. Test: can the sentence be shortened without losing meaning?

**Information density**
Flag sentences or paragraphs where little or no new information is delivered: restatements of what a heading already says, throat-clearing introductions, and transition sentences that describe what the next paragraph will say.

**Scanability**
Flag:
* Paragraphs longer than 5 sentences that could be lists
* Sections with no visual break between dense prose blocks
* Missing or weak lead sentences that do not orient the reader

**Redundancy**
Flag content that appears more than once. Note both locations.

**Voice**
Flag passive constructions. Note when passive may be justified (actor is unknown or irrelevant).

**Heading quality**
Flag headings that:
* Are vague ("Overview," "More information," "Details")
* Do not match the content type. Task sections use action verbs. Concept sections use noun phrases.

**Action clarity**
For procedural sections, flag instructions that are ambiguous, incomplete, or missing an explicit outcome. A good instruction tells the reader what to do and what to expect when they have done it.

**Progressive disclosure**
Flag when information appears before the reader needs it. Background and context should follow actionable content, not precede it.

**Consistency**
Flag places where the page contradicts itself, for example a table and a paragraph that describe the same permission differently.

**Style guide compliance**
Flag violations of the project instruction file that the lint script cannot catch, such as tone, terminology, and required page elements.

**AI-sounding phrasing**
Flag phrasing that reads as generated even without a banned word: empty openers, stacked adjectives, a list of three where one item would do, and sentences that announce what the next sentence will say.

### Step 3: Cold-reader check

Spawn a sub-agent with no context from this conversation. Give it only the document content and these four questions:

1. What does this doc help you do?
1. Who is it written for?
1. What is the first thing you should do after reading it?
1. What is still unclear?

If the sub-agent's answers do not match the doc's stated purpose, that is a finding. Report what it got wrong and which section caused the confusion.

### Step 4: Write the report

In ticket mode, write the report to `.claude/workspace/[TICKET-ID]/review.md`. With a file path, output it in the conversation.

Use these sections, in this order:

```markdown
# Review: [TICKET-ID or file name]

## Mechanical findings
Lint findings you kept in Step 1.

## Structural findings
Findings from Step 2.

## Technical verification
The number of GAP and VERIFY markers left in the file, and each one with its line number.

## Cold-reader result
The sub-agent's four answers, and any place they did not match the doc's purpose.

## Pre-existing issues
| File | Line | Severity | Issue |
|---|---|---|---|

## Summary
One paragraph: whether the doc is ready to publish, the single most important fix,
a count of findings by severity, and the number of markers left.
```

Leave out a section only if it has nothing in it, and say so in one line, for example "No pre-existing issues."

Write each finding in the Mechanical and Structural sections in this format:

```markdown
### [Line number or section name]: [Issue type]

* **Severity:** Critical | Major | Minor
* **Confidence:** High | Medium | Low
* **Problem:** [What is wrong and why it hurts the reader]
* **Suggested rewrite:** [Improved version, or "N/A: structural issue"]
```

Order findings by severity (Critical first), then by position in the document.

## Example finding

```markdown
### Introduction: AI-generated phrasing + style violation

* **Severity:** Critical
* **Confidence:** High
* **Problem:** "It's worth noting" is AI-generated filler and adds no information. "Utilize" should be "use" per the style guide. The opening sentence is 38 words and restates the page title without adding meaning.
* **Suggested rewrite:** Use rate limiting to control how many requests the API accepts within a given time window.
```

## Output

* Ticket ID: `.claude/workspace/[TICKET-ID]/review.md`
* File path: the report in the conversation

## Severity definitions

* **Critical:** Must fix before publish. Style guide violation or broken instruction.
* **Major:** Fix before publish. Significantly hurts clarity or consistency.
* **Minor:** Improvement opportunity. Writer's discretion.

## Confidence definitions

* **High:** Objectively wrong per the style guide.
* **Medium:** Clear pattern match, but context could justify the choice.
* **Low:** Judgment call. The writer may have good reason for it.

## Rules

* Do not verify factual accuracy. That is the writer's responsibility.
* Do not question structure or doc type decisions. Those were made in `plan-doc`.
* Do not resolve or remove GAP and VERIFY markers. Count and list them.
* Do not rewrite large sections unprompted. Provide findings. Let the writer decide.
* If the writer asks for a rewrite of a specific section after seeing the findings, do it.
