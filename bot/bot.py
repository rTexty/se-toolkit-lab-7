import sys
import argparse
import os

# Use absolute imports relative to this file's folder
from handlers.commands import (
    handle_start, 
    handle_help, 
    handle_health, 
    handle_labs, 
    handle_scores
)
from config import config

def test_mode(query: str):
    parts = query.split()
    cmd = parts[0].lstrip('/')
    args = parts[1:]
    
    if cmd == "start":
        print(handle_start())
    elif cmd == "help":
        print(handle_help())
    elif cmd == "health":
        print(handle_health())
    elif cmd == "labs":
        print(handle_labs())
    elif cmd == "scores":
        lab_id = args[0] if args else None
        print(handle_scores(lab_id))
    else:
        print(f"Unknown command: {cmd}")

def main():
    parser = argparse.ArgumentParser(description="LMS Telegram Bot")
    parser.add_argument("--test", type=str, help="Run a command in test mode and exit")
    args = parser.parse_args()

    if args.test:
        test_mode(args.test)
        sys.exit(0)

    print("Production loop placeholder (no token)")
    sys.exit(0)

if __name__ == "__main__":
    main()
