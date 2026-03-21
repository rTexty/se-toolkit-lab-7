# Development Plan - LMS Telegram Bot

We're building a Telegram bot that talks to your LMS backend. It has slash commands like /health and /labs, and later understands plain text questions using an LLM.

## Phase 1: Basic Scaffolding and Commands
In this phase, we established the basic structure of the Telegram bot using `python-telegram-bot`. We successfully scaffolded a robust `uv`-based Python environment and isolated the core logic from the transport layer. The primary architectural pattern we are relying on is "Separation of Concerns". Handlers simply take string inputs and return string responses, making it entirely possible to test using `--test` mode without hitting the real Telegram network.

## Phase 2: Integration with the Backend Services
We will integrate a robust HTTP client to connect with our remote Fast API backend (`http://localhost:42002`). This includes fetching health statuses, labs items, and student progress/scores. We will correctly pass Bearer authorization tokens fetched from `.env.bot.secret`.

## Phase 3: LLM Intent Routing
For unknown free-form inputs, we will integrate a Large Language Model (Qwen Code Plus) using standard OpenAI API wrappers. The bot will supply tools describing other handlers (e.g. `get_labs`, `get_scores`). If the LLM successfully parses an intent, it calls the correct python function locally and re-routes the user.

## Phase 4: Containerization
We will build a simple `Dockerfile` using the python Alpine image, installing `uv` and setting up the environment. The bot will then be joined to the central `docker-compose.yml` so it runs natively within the `lms-network` next to the server component.

## Architectural Patterns
- Separation of Concerns: Handlers are isolated from the Telegram transport layer. This allows testing without a Telegram connection.
- Service-Oriented Logic: LMS and LLM interactions are encapsulated in dedicated service modules.
- Env-based Configuration: All sensitive data and endpoint URLs are loaded from .env files for security and portability.
- Intent-based Routing: We use an LLM for flexible routing of user requests instead of simple regex or keyword matching.
