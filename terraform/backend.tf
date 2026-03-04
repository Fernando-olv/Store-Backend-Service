terraform {
  backend "gcs" {
    bucket = var.tf_state_bucket
    prefix = "store-backend-service/terraform/state"
  }
}
