# Agent Playbook

## Safe Workflow Order

1. Read `docs/README.md` and linked docs.
2. Inspect relevant code paths.
3. Run non-destructive checks first.
4. Propose/implement minimal changes.
5. Validate behavior locally.
6. Summarize changes + residual risks.

## Environment Assumptions

- Repo root is working directory.
- Local stack can run with Docker + Makefile.
- Terraform uses GCS backend and per-env tfvars.

## Preferred Operational Commands

- App runtime: `make up`, `make health`, `make logs`, `make down`
- Quality: `make test`, `make lint`, `make format`
- Infra: `make tf-init`, `make tf-plan`, `make tf-apply`

## Non-Destructive First Policy

Before mutating code or infra:

- read relevant files,
- inspect current behavior,
- run plan/check commands where possible,
- avoid destructive git/system commands unless explicitly requested.

## Before Changing App Code Checklist

- Confirm endpoint/service/repository path.
- Confirm existing models/status contracts.
- Check local env vars needed for new behavior.
- Add or adjust tests/docs together with behavior changes.

## Before Changing Terraform Checklist

- Confirm variable presence in both `variables.tf` and `envs/dev.tfvars`.
- Confirm provider/API dependencies.
- Verify expected runtime env vars on Cloud Run.
- Run `terraform validate` and a plan before apply.

## Communication Rules for Agents

- Report what changed, why, and how to validate.
- Call out blockers explicitly (permissions, missing tools, auth).
- Do not silently skip failed validation.
