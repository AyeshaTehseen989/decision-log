# 1. Use SQLite for storage

Status: accepted

## Context
The app stores a small number of text records and has one user at a time.
I wanted something easy to run with no extra install.

## Decision
Use SQLite through Python's built-in sqlite3 module, with plain SQL.

## Consequences
- Good: no database server to install, and the code shows exactly what SQL runs.
- Bad: one writer at a time, and the table is created on every connection
  instead of through migrations.
- Revisit if multiple people need to write at the same time.