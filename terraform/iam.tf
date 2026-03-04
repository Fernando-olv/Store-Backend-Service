resource "google_service_account" "runtime" {
  account_id   = substr(replace(local.resource_name, "_", "-"), 0, 30)
  display_name = "${local.resource_name} runtime"
  description  = "Runtime service account for ${local.resource_name}"

  depends_on = [google_project_service.required]
}
