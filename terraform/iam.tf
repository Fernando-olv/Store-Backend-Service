resource "google_service_account" "runtime" {
  account_id   = substr(replace(local.resource_name, "_", "-"), 0, 30)
  display_name = "${local.resource_name} runtime"
  description  = "Runtime service account for ${local.resource_name}"

  depends_on = [google_project_service.required]
}

resource "google_project_iam_member" "runtime_firestore_user" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.runtime.email}"
}
