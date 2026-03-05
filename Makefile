IMAGE_LOCAL := store-backend-service:local
IMAGE_PROD := store-backend-service:prod
DEV_CONTAINER := store-backend-service-dev
PROD_CONTAINER := store-backend-service-prod
LEGACY_CONTAINER := store-backend-local
ENV_FILE := .env
TF_DIR ?= terraform

.PHONY: up down logs health rebuild ps prod prod-down test lint format tf-init tf-plan tf-apply

up:
	@if docker compose version >/dev/null 2>&1; then \
		ENV_OPT=$$( [ -f $(ENV_FILE) ] && echo "--env-file $(ENV_FILE)" ); \
		docker compose $$ENV_OPT up -d --build; \
	else \
		ENV_OPT=$$( [ -f $(ENV_FILE) ] && echo "--env-file $(ENV_FILE)" ); \
		docker build -t $(IMAGE_LOCAL) .; \
		docker rm -f $(LEGACY_CONTAINER) >/dev/null 2>&1 || true; \
		docker rm -f $(DEV_CONTAINER) >/dev/null 2>&1 || true; \
		docker run -d --rm -p 8000:8000 --name $(DEV_CONTAINER) \
			$$ENV_OPT \
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

logs:
	@if docker compose version >/dev/null 2>&1; then \
		docker compose logs -f api; \
	else \
		docker logs -f $(DEV_CONTAINER); \
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
		docker build --no-cache -t $(IMAGE_LOCAL) .; \
		docker rm -f $(LEGACY_CONTAINER) >/dev/null 2>&1 || true; \
		docker rm -f $(DEV_CONTAINER) >/dev/null 2>&1 || true; \
		docker run -d --rm -p 8000:8000 --name $(DEV_CONTAINER) \
			$$ENV_OPT \
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
	docker run -d --rm -p 8000:8000 --name $(PROD_CONTAINER) $$ENV_OPT $(IMAGE_PROD)

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
