---
name: commit-changes
description: Review, validate, stage, and commit intended changes in this Git repository using its documented Conventional Commits policy. Use when the user explicitly asks to commit current work, create a commit, prepare changes for a commit, or make a repository commit after completing a task.
---

# Commit Changes

Create one safe, focused Git commit for the changes the user authorized. Preserve
unrelated work and leave the repository in an understandable state.

## Workflow

1. Read `docs/commit-convention.md` completely. Treat it as the repository's
   authoritative commit policy. If it is absent or ambiguous, stop and tell the
   user what must be resolved.
2. Inspect the repository before staging anything:
   - Run `git status --short`.
   - Review both `git diff` and `git diff --cached`.
   - Inspect relevant untracked files without assuming they belong in the commit.
3. Determine the authorized scope from the user's request and the work performed
   in the current task. Do not include unrelated pre-existing changes. If the
   intended and unrelated changes overlap in the same file and cannot be safely
   separated, ask the user before staging it.
4. Check for secrets, credentials, private keys, machine-local configuration,
   generated artifacts, build outputs, and unexpectedly large or binary files.
   Do not stage suspicious material; report it to the user.
5. Run the smallest relevant formatting, build, and test checks for the intended
   changes. If a required check fails, do not commit unless the user explicitly
   directs otherwise after seeing the failure.
6. Choose a Conventional Commits message that describes the outcome:

   ```text
   <type>[optional scope][!]: <concise imperative description>
   ```

   Use the narrowest suitable type, commonly `feat`, `fix`, `docs`, `test`,
   `build`, `ci`, `refactor`, `perf`, `style`, `chore`, or `revert`. Add a body
   only when it explains important motivation, behavior, or tradeoffs. Mark a
   breaking change with `!` and a `BREAKING CHANGE:` footer.
7. Stage explicit paths with `git add -- <path>...`. Avoid `git add .`, `git add
   -A`, and broad globs when the working tree contains anything outside the
   authorized scope.
8. Re-run `git status --short` and review `git diff --cached`. Confirm that the
   staged patch is coherent, contains only intended files, and matches the commit
   message.
9. Create the commit with `git commit`. Let repository hooks run normally.
10. Verify the result with `git status --short` and inspect the new commit's hash,
    subject, and file summary.

## Guardrails

- Never amend or rewrite an existing commit unless the user explicitly asks.
- Never use `--no-verify`, disable signing, or bypass a repository hook merely to
  make a commit succeed.
- Never push, create a tag, or open a pull request as part of this skill unless
  the user separately requests that action.
- Never discard, restore, reset, stash, or clean changes to prepare the commit
  without explicit user authorization.
- Do not create an empty commit unless the user explicitly requests one.
- If a hook changes files, inspect those changes, rerun relevant checks, and
  review the staged diff again before retrying the commit.
- If nothing appropriate is available to commit, report that fact instead of
  manufacturing a change.

## Handoff

Report the commit hash and subject, the validation performed, and any remaining
uncommitted changes. Clearly state if the commit was not created and why.
