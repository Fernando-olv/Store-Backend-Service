# Conventions

## Naming and Structure

- Keep API layer organized as `routers -> services -> repositories -> models`.
- Place cross-cutting runtime helpers under `app/services`.
- Keep endpoint prefixes resource-oriented (`/auth`, `/products`, `/orders`).

## API Behavior Conventions

- Use clear HTTP status mappings:
  - `401` for invalid credentials
  - `404` for missing resources
  - `409` for business conflicts (e.g., `no_stock`)
  - `422` for input validation errors
- Keep user-facing detail messages short and stable.

## Stock/Order Business Rules

- Order creation must be transactional.
- Stock decrement and order creation should commit atomically.
- Product status derives from quantity (`in_stock` vs `out_of_stock`).

## Dependency Management

Current repo includes both `requirements.txt` and uv artifacts (`pyproject.toml`, `uv.lock`).

Operational default today:

- Runtime/deploy dependency source: `requirements.txt`
- Quality/test tools also listed in `requirements.txt`

If migrating fully to `uv`, update docs and build workflow together in one change.

## Documentation Conventions

- Keep root `README.md` high-level.
- Put implementation/runbook details in `docs/`.
- Keep docs concise and command-oriented for agent execution.
