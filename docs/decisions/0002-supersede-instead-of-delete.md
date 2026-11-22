# 2. Supersede decisions instead of deleting them

Status: accepted

## Context
A decision log is only useful if the history is trustworthy.
Teams change their minds, and deleting the old decision hides why.

## Decision
A decision can be proposed or accepted. When a team changes its mind, the old
decision is marked superseded and linked to the new one. Both changes happen
in one database transaction. Superseded decisions cannot be edited again.

## Consequences
- Good: the full history stays readable, and the data can never end up
  half-updated.
- Bad: there is no way to fix a typo in an old decision.