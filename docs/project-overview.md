# Project Overview

## Mission

Build a store backend service with:

- FastAPI application layer,
- Firestore persistence,
- Terraform-managed GCP infrastructure,
- Cloud Run deployment target.

## Tech Stack

- Python + FastAPI
- Firestore (`google-cloud-firestore`)
- JWT auth (`python-jose`)
- Password hashing (`passlib` + `bcrypt`)
- Docker + Makefile
- Terraform + Google provider

## High-Level Runtime Modes

Local development:

- API runs in Docker,
- Firestore emulator runs locally,
- API points to emulator via `FIRESTORE_EMULATOR_HOST`.

Production:

- API runs on Cloud Run,
- Firestore managed service in GCP,
- runtime auth through service account IAM.

## Repository Map

- `app/`: API code (routers, services, repositories, models)
- `tests/`: pytest tests + demo notebooks for non-technical walkthroughs
- `terraform/`: infrastructure definitions for GCP
- `docker-compose.yml`: local API + emulator runtime
- `Makefile`: primary operational commands
- `.env.example`: required local env variables template

## Core Business Domains

- Users: register/login with JWT issuance
- Products: CRUD with stock and status
- Orders: authenticated creation with transactional stock decrement
