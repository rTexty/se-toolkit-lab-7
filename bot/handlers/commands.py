from services.lms import lms_client

async def handle_start(user_id: int = None) -> str:
    """Welcome the user."""
    return "Welcome to the LMS Telegram Bot!\nUse /help to see my available commands."

async def handle_help() -> str:
    """Show available commands."""
    return (
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/health - Check backend status\n"
        "/labs - List available labs\n"
        "/scores <lab_id> - View your scores"
    )

async def handle_health() -> str:
    """Check backend connectivity."""
    try:
        items = await lms_client.get_items()
        return f"Backend is healthy. {len(items)} items available."
    except Exception as e:
        return str(e)

async def handle_labs() -> str:
    """List labs from the LMS."""
    try:
        items = await lms_client.get_items()
        labs = {}
        for item in items:
            if item.get("type") == "lab":
                labs[item.get("id")] = item.get("title", f"Lab {item.get('id')}")
        
        if not labs:
            return "No labs found in the backend."
        
        lines = ["Available labs:"]
        for lid, name in sorted(labs.items()):
            lines.append(f"- {name}")
        return "\n".join(lines)
    except Exception as e:
        return str(e)

async def handle_scores(lab_id: str = None) -> str:
    """Get student scores for a lab."""
    if not lab_id:
        return "Please specify a lab ID (e.g., /scores lab-1)"
    
    try:
        rates = await lms_client.get_pass_rates(lab_id)
        if not rates:
            return f"No score data found for lab '{lab_id}'."
            
        lines = [f"Pass rates for {lab_id}:"]
        for task in rates:
            name = task.get("task", "Unknown")
            rate = task.get("avg_score", 0)
            attempts = task.get("attempts", 0)
            lines.append(f"- {name}: {rate:.1f}% ({attempts} attempts)")
        return "\n".join(lines)
    except Exception as e:
        return str(e)
