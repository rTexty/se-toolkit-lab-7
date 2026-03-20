# Development Plan - LMS Telegram Bot

We're building a Telegram bot that talks to your LMS backend. It has slash commands like /health and /labs, and later understands plain text questions using an LLM.

## Tasks Overview

### Task 1: Plan and Scaffold
- Establish testable handler architecture.
- Create bot entry point with --test mode.
- Set up project structure and configurations.
- Verify scaffold with placeholder responses.

### Task 2: Backend Integration
- Implement real API calls to the LMS backend.
- Use httpx for asynchronous requests.
- Handle authentication and errors gracefully.
- Support /health, /labs, and /scores with live data.

### Task 3: Intent Routing & LLM
- Implement natural language processing for plain text messages.
- Use an LLM to route user intents to the correct services.
- Define tools (functions) for the LLM to call based on user queries.
- Ensure the bot can answer more complex questions about labs and scores.

### Task 4: Deployment & Docker
- Containerize the bot with Docker.
- Integrate into docker-compose.yml.
- Ensure proper networking with the backend and other services.
- Final verification of the end-to-end functionality.

## Architectural Patterns
- Separation of Concerns: Handlers are isolated from the Telegram transport layer. This allows testing without a Telegram connection.
- Service-Oriented Logic: LMS and LLM interactions are encapsulated in dedicated service modules.
- Env-based Configuration: All sensitive data and endpoint URLs are loaded from .env files for security and portability.
- Intent-based Routing: We use an LLM for flexible routing of user requests instead of simple regex or keyword matching.
