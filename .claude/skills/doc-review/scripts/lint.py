#!/usr/bin/env python3
"""
Mechanical lint for documentation Markdown.

The doc-review skill runs this before its qualitative review. It catches
patterns that do not need judgment, so the review can focus on what does.

Usage:
    python lint.py <path-to-file.md>

To adapt it, edit the CONFIG section below. You should not need to touch
anything under CHECKS.
"""

import re
import sys
from pathlib import Path

# ============================================================================
# CONFIG: fill this in with your team's rules
# ============================================================================

# Skip text inside HTML comments, including GAP and VERIFY markers.
# Markers are notes for the reviewer and are removed before publishing.
SKIP_HTML_COMMENTS = True

# Flag sentences longer than this many words. Set to 0 to turn off.
MAX_SENTENCE_WORDS = 30

# Heading style your team uses.
#   "sentence"  flags headings in title case, like "Configure The Rate Limit"
#   "title"     flags headings in sentence case, like "Configure the rate limit"
#   None        turns the heading check off
HEADING_CASE = "sentence"

# Words that may be capitalized in a sentence-case heading.
# Add your product names, tool names, and acronyms one word at a time,
# for example "Claude" and "Code" for Claude Code.
HEADING_EXCEPTIONS = {
    "API", "CLI", "CSS", "HTML", "HTTP", "HTTPS", "ID", "JSON", "SDK",
    "SQL", "UI", "URL", "XML", "YAML",
    # "YourProduct", "YourFeature",
}

# Bullet marker for unordered lists: "*", "-", or None to turn off.
LIST_MARKER = "*"

# Require "1." for every ordered list item instead of 1. 2. 3.
ORDERED_LIST_ALL_ONES = True

# Characters your team does not use, with the reason shown in the report.
# Delete any line your style guide allows.
BANNED_CHARACTERS = {
    "—": "Em dash. Use a period, a colon, or restructure the sentence.",
    ";": "Semicolon. Split into two sentences.",
    "“": "Smart quote. Use straight quotes.",
    "”": "Smart quote. Use straight quotes.",
}

# Words or phrases to replace, mapped to the replacement.
WORD_SUBSTITUTIONS = {
    "utilize": "use",
    "in order to": "to",
    "click on": "click",
    "allows you to": "direct action language",
    "enables you to": "direct action language",
}

# Words or phrases to avoid: marketing language, filler, AI-sounding phrasing.
AVOID_PHRASES = [
    "seamless", "seamlessly", "robust", "leverage", "powerful", "cutting-edge",
    "delve", "unlock", "empower", "game-changer", "streamline", "harness",
    "comprehensive", "moreover", "furthermore", "in conclusion",
    "very", "really", "simply",
    "it is important to note", "please note that", "it's worth noting",
    "as mentioned above", "needless to say",
]

# Flag "click the X button". Write "click X" instead.
CHECK_BUTTON_LABEL = True

# Flag "This", "That", "These", or "Those" followed directly by a verb.
CHECK_BARE_DEMONSTRATIVES = True

# Flag future tense such as "will be" and "will return".
CHECK_FUTURE_TENSE = True

# Flag passive voice. A passive followed by "by" ("is processed by the gateway")
# is reported as Passive voice. Other matches are reported as Possible passive
# voice. Many of those are fine. Treat them as a prompt to check.
CHECK_PASSIVE_VOICE = True

# Severity for each rule: "Critical", "Major", or "Minor".
SEVERITY = {
    "Banned character": "Critical",
    "Word substitution": "Major",
    "Avoid phrase": "Major",
    "Heading case": "Major",
    "List marker": "Major",
    "Ordered list numbering": "Major",
    "Bare demonstrative": "Major",
    "Button label": "Major",
    "Passive voice": "Major",
    "Future tense": "Minor",
    "Possible passive voice": "Minor",
    "Long sentence": "Minor",
}

# ============================================================================
# CHECKS
# ============================================================================


def blank_keep_lines(match):
    """Replace matched text with the same number of newlines."""
    return "\n" * match.group(0).count("\n")


def prepare(text):
    """Remove content that should not be linted, keeping line numbers intact."""
    # Front matter at the top of the file
    text = re.sub(r"\A---\n.*?\n---\n", blank_keep_lines, text, flags=re.S)
    # Fenced code blocks
    text = re.sub(r"^(```|~~~).*?^\1[^\n]*$", blank_keep_lines, text, flags=re.S | re.M)
    if SKIP_HTML_COMMENTS:
        text = re.sub(r"<!--.*?-->", blank_keep_lines, text, flags=re.S)
    return text.split("\n")


def prose(line):
    """Return a line with inline code and link targets removed."""
    line = re.sub(r"`[^`]*`", " ", line)
    return re.sub(r"\]\([^)]*\)", "]", line)


def is_heading(line):
    return re.match(r"^#{1,6}\s", line) is not None


def is_table(line):
    return line.lstrip().startswith("|")


def phrase_pattern(phrase):
    return re.compile(r"\b" + re.escape(phrase) + r"\b", re.I)


def check_line(number, raw):
    findings = []
    text = prose(raw)
    stripped = text.strip()
    if not stripped:
        return findings

    def add(rule, message):
        findings.append((number, rule, message, raw.strip()))

    for char, reason in BANNED_CHARACTERS.items():
        if char in text:
            add("Banned character", reason)

    for word, replacement in WORD_SUBSTITUTIONS.items():
        if phrase_pattern(word).search(text):
            add("Word substitution", f'Replace "{word}" with {replacement}.')

    for phrase in AVOID_PHRASES:
        if phrase_pattern(phrase).search(text):
            add("Avoid phrase", f'Avoid "{phrase}".')

    if is_heading(raw) and HEADING_CASE:
        words = re.sub(r"^#+\s*", "", stripped).split()
        rest = [w.strip(".,:?!()") for w in words[1:]]
        capitals = [w for w in rest if w[:1].isupper() and w not in HEADING_EXCEPTIONS]
        if HEADING_CASE == "sentence" and len(capitals) >= 2:
            add("Heading case", "Use sentence case. Capitalize only the first word and proper nouns.")
        if HEADING_CASE == "title" and len(rest) >= 2 and not capitals:
            add("Heading case", "Use title case.")

    if LIST_MARKER:
        other = "-" if LIST_MARKER == "*" else "*"
        if re.match(r"^\s*" + re.escape(other) + r"\s+\S", raw):
            add("List marker", f'Use "{LIST_MARKER}" for unordered list items.')

    if ORDERED_LIST_ALL_ONES and re.match(r"^\s*([2-9]|\d{2,})\.\s+\S", raw):
        add("Ordered list numbering", 'Use "1." for every ordered list item.')

    if CHECK_BUTTON_LABEL and re.search(r"\bclick\s+the\s+[*_`]*[\w][\w\s]*?[*_`]*\s+button\b", text, re.I):
        add("Button label", 'Write "click X", not "click the X button".')

    if CHECK_BARE_DEMONSTRATIVES and re.search(
        r"\b(This|That|These|Those)\s+(is|are|was|were|will|can|means|makes|"
        r"lets|allows|enables|prevents|ensures|helps|shows|returns|creates)\b", text
    ):
        add("Bare demonstrative", 'Follow "This" or "That" with a noun: "This value prevents", not "This prevents".')

    if is_heading(raw) or is_table(raw):
        return findings

    if CHECK_FUTURE_TENSE and re.search(r"\bwill\s+(be|have|return|create|show|allow|need)\b", text, re.I):
        add("Future tense", "Use present tense.")

    if CHECK_PASSIVE_VOICE:
        if re.search(r"\b(is|are|was|were|be|been|being)\s+\w+ed\s+by\b", text, re.I):
            add("Passive voice", 'Rewrite so the subject after "by" does the action.')
        elif re.search(r"\b(is|are|was|were|be|been|being)\s+\w+ed\b", text, re.I):
            add("Possible passive voice", "Check whether an active subject would be clearer.")

    if MAX_SENTENCE_WORDS:
        for sentence in re.split(r"(?<=[.!?])\s+", stripped):
            count = len(re.findall(r"\b[\w'-]+\b", sentence))
            if count > MAX_SENTENCE_WORDS:
                add("Long sentence", f"{count} words. Split or trim to {MAX_SENTENCE_WORDS} or fewer.")
                break

    return findings


# ============================================================================
# REPORT
# ============================================================================

ORDER = {"Critical": 0, "Major": 1, "Minor": 2}


def main():
    # Print UTF-8 on every platform, including the Windows console.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if len(sys.argv) != 2:
        print("Usage: python lint.py <path-to-file.md>")
        sys.exit(2)

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"File not found: {path}")
        sys.exit(2)

    # utf-8-sig drops the byte-order mark some Windows editors add at the start of a file.
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    findings = []
    for number, line in enumerate(prepare(text), start=1):
        findings.extend(check_line(number, line))

    if not findings:
        print(f"No mechanical issues found in {path}")
        return

    rows = sorted(
        ((SEVERITY.get(rule, "Minor"), number, rule, message, line)
         for number, rule, message, line in findings),
        key=lambda row: (ORDER[row[0]], row[1]),
    )
    counts = {level: sum(1 for row in rows if row[0] == level) for level in ORDER}

    print(f"Lint: {path}")
    print(f"Critical: {counts['Critical']}  Major: {counts['Major']}  Minor: {counts['Minor']}")
    print()
    for severity, number, rule, message, line in rows:
        print(f"[{severity}] Line {number}: {rule}")
        print(f"  Text: {line[:100]}")
        print(f"  Fix:  {message}")
        print()

    # Exit 1 when there are Critical findings, so the script can gate a CI job later.
    sys.exit(1 if counts["Critical"] else 0)


if __name__ == "__main__":
    main()
