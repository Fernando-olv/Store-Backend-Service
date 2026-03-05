# Store Backend Service

Store Backend Service is a backend project for a store platform.

The main idea is to build and manage the infrastructure using Terraform on Google Cloud, while the application layer is implemented in Python.

## Tech Stack

- Python (FastAPI)
- Terraform
- Google Cloud Platform (GCP)
- Docker

## Project Goal

Create a backend service that can grow safely with infrastructure as code, clear service organization, and support for cloud deployment.

## Local Development (Docker)

### Prerequisites

- Docker installed and running
- Your user has access to Docker daemon (`docker` group)

### Quickstart (recommended)

```bash
make up
make health
```

Expected response:

```json
{"status":"ok"}
```

Useful commands:

```bash
make logs
make ps
make down
```

### Production-like local run (no reload mount)

```bash
make prod
make health
make prod-down
```
