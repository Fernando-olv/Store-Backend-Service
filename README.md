# Store Backend Service

Stage 0 scaffold for a Python backend service with Terraform (GCP).

## Project Structure

```text
store-backend-service/
├── terraform/
│   ├── backend.tf
│   ├── provider.tf
│   └── variables.tf
├── app/
│   ├── main.py
│   ├── routers/
│   ├── services/
│   ├── models/
│   └── repositories/
├── functions/
│   └── send_email/
├── tests/
├── Dockerfile
├── requirements.txt
└── README.md
```

## Stage 0 Tasks

### 1) Create GitHub repository

```bash
git init
git add .
git commit -m "chore: stage 0 project scaffold"
git branch -M main
git remote add origin git@github.com:<your-user>/store-backend-service.git
git push -u origin main
```

### 2) Install tooling

Required tools:
- Python 3.12+
- Terraform 1.6+
- Google Cloud SDK (`gcloud`)
- Docker (optional for local container run)

Create local Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3) Configure GCP project

```bash
gcloud auth login
gcloud projects create <PROJECT_ID> --name="store-backend-service"
gcloud config set project <PROJECT_ID>
gcloud services enable cloudresourcemanager.googleapis.com iam.googleapis.com compute.googleapis.com
```

Create bucket for Terraform remote state:

```bash
gsutil mb -p <PROJECT_ID> -l us-central1 gs://<TF_STATE_BUCKET>
gsutil versioning set on gs://<TF_STATE_BUCKET>
```

### 4) Configure Terraform backend

From `terraform/`, initialize using backend config values:

```bash
cd terraform
terraform init \
  -backend-config="bucket=<TF_STATE_BUCKET>" \
  -backend-config="prefix=store-backend-service/terraform/state"
```

Optional local `terraform.tfvars`:

```hcl
gcp_project_id = "<PROJECT_ID>"
gcp_region     = "us-central1"
tf_state_bucket = "<TF_STATE_BUCKET>"
```

## Run app locally

```bash
uvicorn app.main:app --reload
```

Health check: `GET /health`
