# 3. Separate Python API and React frontend

Status: accepted

## Context
The listing for this role uses Python and React, and I wanted to practise
both on one small project.

## Decision
FastAPI serves a JSON API. A React app (Vite) calls it with fetch. CORS allows
only the frontend's address.

## Consequences
- Good: each side can be tested and changed on its own.
- Bad: two servers to run in development.