def handle_start(user_id: int = None) -> str:
    """Welcome the user."""
    return "Welcome to the LMS Telegram Bot!\nUse /help to see my available commands."

def handle_help() -> str:
    """Show available commands."""
    return (
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/health - Check backend status\n"
        "/labs - List available labs\n"
        "/scores <lab_id> - View your scores"
    )

def handle_health() -> str:
    """Check backend connectivity."""
    return "Checking backend connectivity... (Task 2 will implement this)"

def handle_labs() -> str:
    """List labs from the LMS."""
    return "Fetching available labs... (Task 2 will implement this)"

def handle_scores(lab_id: str = None) -> str:
    """Get student scores for a lab."""
    if not lab_id:
        return "Please specify a lab ID (e.g., /scores lab-1)"
    return f"Getting scores for {lab_id}... (Task 2 will implement this)"
