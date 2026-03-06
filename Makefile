IMAGE_LOCAL := store-backend-service:local
IMAGE_PROD := store-backend-service:prod
DEV_CONTAINER := store-backend-service-dev
PROD_CONTAINER := store-backend-service-prod
LEGACY_CONTAINER := store-backend-local
EMULATOR_CONTAINER := store-backend-firestore-emulator
ENV_FILE := .env
TF_DIR ?= terraform
FIRESTORE_PROJECT_ID ?= store-backend-local
JWT_SECRET ?= change-me-local
JWT_EXPIRATION_MINUTES ?= 60

.PHONY: up down logs emulator-logs health rebuild ps prod prod-down test lint format tf-init tf-plan tf-apply seed-products

up:
	@if docker compose version >/dev/null 2>&1; then \
		ENV_OPT=$$( [ -f $(ENV_FILE) ] && echo "--env-file $(ENV_FILE)" ); \
		docker compose $$ENV_OPT up -d --build; \
	else \
		ENV_OPT=$$( [ -f $(ENV_FILE) ] && echo "--env-file $(ENV_FILE)" ); \
		docker rm -f $(EMULATOR_CONTAINER) >/dev/null 2>&1 || true; \
		docker run -d --rm -p 8080:8080 --name $(EMULATOR_CONTAINER) \
			-e CLOUDSDK_CORE_PROJECT=$(FIRESTORE_PROJECT_ID) \
			gcr.io/google.com/cloudsdktool/google-cloud-cli:emulators \
			gcloud beta emulators firestore start --host-port=0.0.0.0:8080 --project=$(FIRESTORE_PROJECT_ID) --quiet; \
		docker build -t $(IMAGE_LOCAL) .; \
		docker rm -f $(LEGACY_CONTAINER) >/dev/null 2>&1 || true; \
		docker rm -f $(DEV_CONTAINER) >/dev/null 2>&1 || true; \
		docker run -d --rm -p 8000:8000 --name $(DEV_CONTAINER) \
			$$ENV_OPT \
			--add-host=host.docker.internal:host-gateway \
			-e FIRESTORE_EMULATOR_HOST=host.docker.internal:8080 \
			-e FIRESTORE_PROJECT_ID=$(FIRESTORE_PROJECT_ID) \
			-e JWT_SECRET=$(JWT_SECRET) \
			-e JWT_EXPIRATION_MINUTES=$(JWT_EXPIRATION_MINUTES) \
			-v $$(pwd)/app:/app/app \
			$(IMAGE_LOCAL) \
			uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload; \
	fi

down:
	@if docker compose version >/dev/null 2>&1; then \
		docker compose down --remove-orphans; \
	fi
	docker rm -f $(DEV_CONTAINER) >/dev/null 2>&1 || true
	docker rm -f $(PROD_CONTAINER) >/dev/null 2>&1 || true
	docker rm -f $(LEGACY_CONTAINER) >/dev/null 2>&1 || true
	docker rm -f $(EMULATOR_CONTAINER) >/dev/null 2>&1 || true

logs:
	@if docker compose version >/dev/null 2>&1; then \
		docker compose logs -f api; \
	else \
		docker logs -f $(DEV_CONTAINER); \
	fi

emulator-logs:
	@if docker compose version >/dev/null 2>&1; then \
		docker compose logs -f firestore-emulator; \
	else \
		docker logs -f $(EMULATOR_CONTAINER); \
	fi

health:
	curl -i --retry 10 --retry-all-errors --retry-delay 1 --retry-connrefused --max-time 20 http://localhost:8000/health

rebuild:
	@if docker compose version >/dev/null 2>&1; then \
		ENV_OPT=$$( [ -f $(ENV_FILE) ] && echo "--env-file $(ENV_FILE)" ); \
		docker compose $$ENV_OPT build --no-cache; \
		docker compose $$ENV_OPT up -d; \
	else \
		ENV_OPT=$$( [ -f $(ENV_FILE) ] && echo "--env-file $(ENV_FILE)" ); \
		docker rm -f $(EMULATOR_CONTAINER) >/dev/null 2>&1 || true; \
		docker run -d --rm -p 8080:8080 --name $(EMULATOR_CONTAINER) \
			-e CLOUDSDK_CORE_PROJECT=$(FIRESTORE_PROJECT_ID) \
			gcr.io/google.com/cloudsdktool/google-cloud-cli:emulators \
			gcloud beta emulators firestore start --host-port=0.0.0.0:8080 --project=$(FIRESTORE_PROJECT_ID) --quiet; \
		docker build --no-cache -t $(IMAGE_LOCAL) .; \
		docker rm -f $(LEGACY_CONTAINER) >/dev/null 2>&1 || true; \
		docker rm -f $(DEV_CONTAINER) >/dev/null 2>&1 || true; \
		docker run -d --rm -p 8000:8000 --name $(DEV_CONTAINER) \
			$$ENV_OPT \
			--add-host=host.docker.internal:host-gateway \
			-e FIRESTORE_EMULATOR_HOST=host.docker.internal:8080 \
			-e FIRESTORE_PROJECT_ID=$(FIRESTORE_PROJECT_ID) \
			-e JWT_SECRET=$(JWT_SECRET) \
			-e JWT_EXPIRATION_MINUTES=$(JWT_EXPIRATION_MINUTES) \
			-v $$(pwd)/app:/app/app \
			$(IMAGE_LOCAL) \
			uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload; \
	fi

ps:
	@if docker compose version >/dev/null 2>&1; then \
		docker compose ps; \
	else \
		docker ps --filter name=$(DEV_CONTAINER) --filter name=$(PROD_CONTAINER); \
	fi

prod:
	ENV_OPT=$$( [ -f $(ENV_FILE) ] && echo "--env-file $(ENV_FILE)" ); \
	docker build -t $(IMAGE_PROD) .; \
	docker rm -f $(LEGACY_CONTAINER) >/dev/null 2>&1 || true; \
	docker rm -f $(PROD_CONTAINER) >/dev/null 2>&1 || true; \
	docker rm -f $(EMULATOR_CONTAINER) >/dev/null 2>&1 || true; \
	docker run -d --rm -p 8000:8000 --name $(PROD_CONTAINER) \
		$$ENV_OPT \
		-e FIRESTORE_PROJECT_ID=$(FIRESTORE_PROJECT_ID) \
		-e JWT_SECRET=$(JWT_SECRET) \
		-e JWT_EXPIRATION_MINUTES=$(JWT_EXPIRATION_MINUTES) \
		$(IMAGE_PROD)

prod-down:
	docker rm -f $(PROD_CONTAINER) >/dev/null 2>&1 || true

test:
	pytest

lint:
	ruff check .

format:
	ruff format .

tf-init:
	cd $(TF_DIR) && terraform init

tf-plan:
	cd $(TF_DIR) && terraform plan

tf-apply:
	cd $(TF_DIR) && terraform apply

seed-products:
	curl -s -X POST http://localhost:8000/products \
		-H "Content-Type: application/json" \
		-d '{"product_id":"p001","product_name":"Sample Product","quantity":10}'
