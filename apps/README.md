# Apps Directory (`/apps`)

This directory is an organizational **Workspace Boundary** using a monorepo approach.

## Purpose

By keeping applications strictly within `/apps/`, the repository root remains clean, language-agnostic, and purely structural. It explicitly forbids the installation of global language dependencies (e.g. `package.json`, `mix.exs`, `requirements.txt`) at the repository root.

## Structure

Each application inside this directory is considered a fully standalone project with its own tooling, tests, dependencies, and configuration layers.

**Python/JS Stack Example (Monorepo):**
- `/apps/frontend/` (The actual source code for the SvelteKit application)
- `/apps/backend/` (The independent configuration and domains for the FastAPI service)

**BEAM/Elixir Stack Example (Umbrella):**
- `/apps/my_app/` (The backend core logic layer)
- `/apps/my_app_web/` (The standalone Phoenix web layer)

## What Goes Here
- Client-facing web applications
- Mobile applications
- Desktop applications
- Backend API services (e.g. `apps/backend/`)
- Background workers and message processors

## What Does NOT Go Here
- **Global Manifests:** Global language dependencies must never be hoisted out of `/apps/` to the repository root.
