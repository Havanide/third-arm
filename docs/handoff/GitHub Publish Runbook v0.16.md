# GitHub Publish Runbook v0.16

## Goal
Publish the local Third Arm repo to GitHub with minimal friction, while preserving the new CI/test baseline and keeping the repo ready for Claude Code and Codex review loops.

## Recommended repo name
`third-arm`

## What is already prepared in the repo
- `.github/workflows/python-ci.yml` — test workflow for push and pull request.
- `.github/pull_request_template.md` — review structure with Stage/BOM impact.
- `tests/conftest.py` — makes raw checkout test execution reliable.

## Publish path A — GitHub web UI + terminal
1. Create a new empty repository on GitHub (do **not** initialize it with README / .gitignore / license if your local repo already has them).
2. In the local repo root run:

```bash
git init
git add .
git commit -m "chore: bootstrap third-arm repo for stage1"
git branch -M main
git remote add origin https://github.com/<YOUR_USER>/<YOUR_REPO>.git
git push -u origin main
```

## Publish path B — GitHub CLI
If `gh` is installed and authenticated:

```bash
git init
git add .
git commit -m "chore: bootstrap third-arm repo for stage1"
gh repo create <YOUR_REPO> --private --source=. --remote=origin --push
```

## Recommended repo settings right after first push
- Default branch: `main`
- Actions: enabled
- Pull requests: enabled
- Branch protection for `main`: require PR before merge once the first stable loop is in place
- Optional: require status check `Python CI / test`

## Practical note
Do not block first publication on perfect issue templates, labels, CODEOWNERS, or branch rules. The first real value is getting commit history online and having CI catch obvious breakage.
