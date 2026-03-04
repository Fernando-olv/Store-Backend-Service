resource "google_artifact_registry_repository" "docker" {
  project       = var.project_id
  location      = var.region
  repository_id = local.resource_name
  description   = "Docker images for ${local.resource_name}"
  format        = "DOCKER"

  labels = local.common_labels

  depends_on = [google_project_service.required]
}
