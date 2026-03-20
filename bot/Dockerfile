# Use a slim Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set the working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-install-project --no-dev

# Copy the application code
COPY . .

# Install the project
RUN uv sync --frozen --no-dev

# Set environment variables
ENV PATH="/app/.venv/bin:/Users/rtexty/Library/Application Support/Code/User/globalStorage/github.copilot-chat/debugCommand:/Users/rtexty/Library/Application Support/Code/User/globalStorage/github.copilot-chat/copilotCli:/root/.vscode-server/cli/servers/Stable-ce099c1ed25d9eb3076c11e4a280f3eb52b4fbeb/server/bin/remote-cli:/root/.local/bin:/root/.nix-profile/bin:/nix/var/nix/profiles/default/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"
ENV PYTHONPATH="/app"

# Command to run the bot
CMD ["python", "bot.py"]
