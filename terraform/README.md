# Terraform - Stage 1 (Cloud Run Dev)

This stack deploys the Store Backend Service to Cloud Run in `dev` on GCP.

## What it creates

- Required project APIs (including Firestore API)
- Runtime service account
- Runtime service account IAM role `roles/datastore.user`
- Artifact Registry Docker repository
- Cloud Run service
- Optional public invoker IAM binding (`allUsers`)

## Prerequisites

- Terraform >= 1.6
- `gcloud` authenticated
- ADC configured (`gcloud auth application-default login`)
- Existing remote state bucket
- Firestore database initialized in project

## 1) Initialize backend

```bash
terraform init -reconfigure \
  -backend-config="bucket=directed-relic-489223-a2-tfstate" \
  -backend-config="prefix=store-backend-service/terraform/state"
```

## 2) Plan

```bash
terraform plan -var-file=envs/dev.tfvars
```

## 3) Apply

```bash
terraform apply -var-file=envs/dev.tfvars
```

## 4) Build and push image

```bash
gcloud auth configure-docker us-central1-docker.pkg.dev

docker build -t us-central1-docker.pkg.dev/directed-relic-489223-a2/store-backend-service-dev/store-backend-service:dev ..
docker push us-central1-docker.pkg.dev/directed-relic-489223-a2/store-backend-service-dev/store-backend-service:dev
```

Then apply again:

```bash
terraform apply -var-file=envs/dev.tfvars
```

## 5) Verify health endpoint

```bash
SERVICE_URL=$(terraform output -raw cloud_run_service_url)
curl "$SERVICE_URL/health"
```

## Notes

- `jwt_secret` is required by Terraform (`envs/dev.tfvars`).
- Stage 1 keeps `allow_unauthenticated = true` for simple external testing.
- `disable_project_apis_on_destroy = true` in `envs/dev.tfvars` makes `terraform destroy` disable managed APIs.
- Remote state bucket is bootstrap infrastructure and is not managed by this root module.
