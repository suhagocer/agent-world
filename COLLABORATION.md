# Agent World — Multi-Model Collaboration Protocol

## Purpose

This repository is the common reference point for the Agent World collaboration.

## Participants

- ChatGPT — synthesis / coordination support
- Claude — analysis / gap inventory
- Gemini — vision / alternative directions
- DeepSeek — engineering / algorithms
- Grok — critique / simplification / risk review
- Human project owner — final strategic decision authority

These roles are working roles, not exclusive capabilities.

## Workflow

1. A model proposes an idea or analysis.
2. The other models may inspect and challenge it.
3. Evidence and disagreements are preserved.
4. A human decision is made when a decision is required.
5. The decision is recorded in `decisions/`.
6. Accepted implementation work moves into architecture, source code, tests and research as appropriate.

## Rules

- Do not treat one model's analysis as established fact.
- Preserve minority opinions and unresolved contradictions.
- Do not silently overwrite historical analysis.
- Record superseded decisions instead of deleting their history.
- Never commit secrets, API keys, access tokens or private credentials.
- Public repository means all committed content is public.

## GitHub usage

For collaborative code changes, prefer branches + pull requests rather than direct edits to main when practical. Documentation may be updated directly when low-risk and clearly scoped.
