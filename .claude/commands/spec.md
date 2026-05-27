Read the GitHub Issue with number $ARGUMENTS and use it as working context.

Run in sequence:
- `gh issue view $ARGUMENTS`
- `gh issue view $ARGUMENTS --comments`

Present the information with this structure:

## Summary
Number, title, status, assignee, labels.

## Verification
Confirm it has the `spec-approved` label. If it does not, warn that the spec is not approved: reading or discussing the spec can continue, but implementation cannot start.

## Context and objective
Problem it solves and objective in one sentence.

## Expected behavior
- **Input:** what the system receives (type, format, example)
- **Output:** what it produces (type, format, example)
- **Main flow:** numbered steps

## Acceptance criteria
Full list with checkboxes. If any criterion is unclear, flag it.

## Edge cases and errors
Full list of edge scenarios.

## Open questions
If there are unanswered questions, warn that they must be resolved before coding.

## Design notes
Technical constraints, dependencies and relevant decisions.

## Issue comments
Show comments with important decisions or clarifications made during the spec review.

---
When done, indicate you are ready to implement and wait for instructions.
