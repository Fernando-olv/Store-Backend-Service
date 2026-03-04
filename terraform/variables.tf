variable "project_id" {
  description = "GCP project ID where resources will be created"
  type        = string
}

variable "region" {
  description = "Default GCP region"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Deployment environment name"
  type        = string
  default     = "dev"
}

variable "service_name" {
  description = "Base service name"
  type        = string
  default     = "store-backend-service"
}

variable "container_image" {
  description = "Container image URL, including tag"
  type        = string
}

variable "container_port" {
  description = "Container port exposed by the app"
  type        = number
  default     = 8000
}

variable "allow_unauthenticated" {
  description = "Whether Cloud Run service allows unauthenticated access"
  type        = bool
  default     = true
}

variable "min_instances" {
  description = "Minimum Cloud Run instances"
  type        = number
  default     = 0
}

variable "max_instances" {
  description = "Maximum Cloud Run instances"
  type        = number
  default     = 2
}

variable "cpu" {
  description = "CPU limit per Cloud Run instance"
  type        = string
  default     = "1"
}

variable "memory" {
  description = "Memory limit per Cloud Run instance"
  type        = string
  default     = "512Mi"
}

variable "disable_project_apis_on_destroy" {
  description = "Disable managed project APIs when running terraform destroy"
  type        = bool
  default     = true
}
