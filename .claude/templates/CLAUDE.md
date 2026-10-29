# [Project name]

## What this project is
[One paragraph: what you are documenting, who the audience is.]

## Primary goals
When editing documentation, prioritize:
1. Accuracy
1. Clarity
1. Consistency with existing docs
1. Minimal diffs

Do not introduce stylistic rewrites unless explicitly asked.
Prefer small targeted edits over large rewrites.

## Repository structure
* `content/`: documentation source files
* `content/en/`: primary language content
* `[other directories]`: describe your layout

## Writing style rules
[List your non-negotiable rules. Be specific.]
* Never use em dashes
* Never use semicolons
* Sentence case for all headings
* Unordered lists: use *, never -
* Ordered lists: use 1. for every item
* No bare demonstrative pronouns: "This value prevents..." not "This prevents..."
* No marketing language: avoid powerful, seamless, robust, unlock, leverage

## Front matter
[Required fields and what each means. What the agent may and may not change.]

## Special syntax
[Any non-standard Markdown your site uses: shortcodes, custom components, etc.]

## What the agent may do without being asked
* Fix typos
* Fix broken Markdown formatting
* Apply style rules listed above
* Normalize heading case

## What the agent must not do without being asked
* Change product behavior descriptions
* Modify parameter names or code examples
* Rewrite large sections
* Remove or reorder front matter fields

## When uncertain
If product behavior is unclear from the source material, insert:
<!-- VERIFY: [describe what needs confirmation] -->

If information is missing and the doc cannot be completed without it:
<!-- GAP: [describe what is missing] -->
