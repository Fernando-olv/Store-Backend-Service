# Troubleshooting

## 1) Terraform asks for `var.container_image`

Cause:
- apply/plan was run without `-var-file=envs/dev.tfvars` or missing variable value.

Fix:
- `cd terraform && terraform apply -var-file=envs/dev.tfvars`

## 2) Cloud Run deploy fails with "image not found"

Cause:
- image tag not pushed to Artifact Registry.

Fix:
1. Build image
2. Tag with Artifact Registry URL
3. Push image
4. Re-run Terraform apply

## 3) Local emulator fails to start with Java error

Cause:
- using a Cloud SDK image without emulator/runtime support.

Fix:
- use `gcr.io/google.com/cloudsdktool/google-cloud-cli:emulators`

## 4) Docker compose command unavailable

Cause:
- host Docker package lacks compose plugin.

Fix:
- Makefile fallback path runs direct `docker run` commands.

## 5) Auth/register returns 500 with bcrypt/passlib error

Cause:
- bcrypt version incompatibility.

Fix:
- pin `bcrypt==4.0.1` (already in requirements).

## 6) Tests fail with `No module named app`

Cause:
- running tests outside repo root or missing pytest config.

Fix:
- run from repo root and use `pytest.ini` (`pythonpath = .`).

## 7) ImportError for `datetime.UTC`

Cause:
- Python < 3.11.

Fix:
- use `timezone.utc` (already applied in code).
