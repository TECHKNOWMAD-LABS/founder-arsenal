# Contributing to Founder Arsenal

## Adding a New Skill

1. Create `skills/{skill-name}/SKILL.md` with standard frontmatter:
   ```yaml
   ---
   name: "skill-name"
   description: "..."
   license: MIT
   metadata:
     version: 1.0.0
     author: TechKnowmad AI
     category: ...
     domain: ...
     updated: YYYY-MM-DD
   ---
   ```
2. Add keyword triggers and operating modes inside the SKILL.md
3. Register the skill in the root `SKILL.md` dispatch table
4. Add an entry to `CHANGELOG.md`

## Updating a Skill

- Bump `metadata.version` (semver)
- Update `metadata.updated` date
- Add a `CHANGELOG.md` entry under the current date

## Reference Data

Shared reference files live in `reference/`. They are India-specific or cross-skill data assets. When a skill needs shared data:
- Add the file to `reference/`
- Link it from the skill's SKILL.md

## Style Guide

- Use plain Markdown — no HTML
- Tables for structured data (triggers, modes, playbooks)
- Lead with the actionable content, not preamble
- No placeholder company names, addresses, or CIN numbers

## Testing

- Load the skill in Claude Code and run representative prompts
- Verify the dispatcher routes correctly
- Check India-specific references for accuracy

## Pull Requests

- One skill or feature per PR
- Reference the changelog entry in the PR description
- Production-quality: no stubs, no TODOs left in shipped content
