project_id = "directed-relic-489223-a2"
region     = "us-central1"

environment  = "dev"
service_name = "store-backend-service"

container_image = "us-central1-docker.pkg.dev/directed-relic-489223-a2/store-backend-service-dev/store-backend-service:dev"

container_port         = 8000
allow_unauthenticated  = true
min_instances          = 0
max_instances          = 2
cpu                    = "1"
memory                 = "512Mi"
disable_project_apis_on_destroy = true
jwt_secret             = "change-me-in-prod"
