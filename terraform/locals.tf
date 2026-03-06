locals {
  resource_name = "${var.service_name}-${var.environment}"

  common_labels = {
    service    = "store-backend-service"
    env        = var.environment
    managed_by = "terraform"
  }

  required_apis = toset([
    "run.googleapis.com",
    "artifactregistry.googleapis.com",
    "cloudbuild.googleapis.com",
    "iam.googleapis.com",
    "firestore.googleapis.com"
  ])
}
