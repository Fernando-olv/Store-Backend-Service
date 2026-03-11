# Infrastructure Terraform

## Folder

Infrastructure lives in `terraform/`.

## Core Commands

From repo root:

- `make tf-init`
- `make tf-plan`
- `make tf-apply`

Or directly:

- `cd terraform && terraform init`
- `cd terraform && terraform plan -var-file=envs/dev.tfvars`
- `cd terraform && terraform apply -var-file=envs/dev.tfvars`

## Required Inputs

Important variables in this project include:

- `project_id`
- `region`
- `container_image`
- `jwt_secret`

## Cloud Run Image Requirement

`container_image` must be a pushed Artifact Registry URL, not a Dockerfile path.

Example:

`us-central1-docker.pkg.dev/<project>/<repo>/<image>:<tag>`

## Firestore in Infra

Current Terraform configuration includes:

- Firestore API enablement (`firestore.googleapis.com`)
- Cloud Run runtime service account role: `roles/datastore.user`
- Cloud Run env vars:
  - `FIRESTORE_PROJECT_ID`
  - `JWT_SECRET`
  - `JWT_EXPIRATION_MINUTES`

## Backend State

- Remote state backend is GCS.
- Backend bucket itself is bootstrap infra, managed outside this root module.
