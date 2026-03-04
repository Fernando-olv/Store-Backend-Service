variable "gcp_project_id" {
  description = "GCP project ID where resources will be created"
  type        = string
}

variable "gcp_region" {
  description = "Default GCP region"
  type        = string
  default     = "us-central1"
}

variable "tf_state_bucket" {
  description = "GCS bucket name for Terraform remote state"
  type        = string
}
