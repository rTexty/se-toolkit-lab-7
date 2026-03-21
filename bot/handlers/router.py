import json
import sys
from services.llm import llm_client
from services.lms import lms_client

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_items",
            "description": "Get all labs and tasks from the LMS. Use this to find lab-01, lab-02 identifiers.",
            "parameters": {"type": "object", "properties": {}},
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_pass_rates",
            "description": "Get per-task average scores and attempt counts for a specific lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab ID, e.g. 'lab-01'"}
                },
                "required": ["lab"],
            }
        }
    }
,
    {
        "type": "function",
        "function": {
            "name": "get_learners",
            "description": "Get all learners from the LMS.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "enroll_learner",
            "description": "Enroll a learner in the LMS.",
            "parameters": {"type": "object", "properties": {"learner_name": {"type": "string"}}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_active_sprint",
            "description": "Get current active sprint.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_course_info",
            "description": "Information about the course.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_lab_status",
            "description": "Update the status of a lab.",
            "parameters": {"type": "object", "properties": {"lab_id": {"type": "string"}}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_system_health",
            "description": "Check if the backend is alive.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_profile",
            "description": "Get profile of a specific user.",
            "parameters": {"type": "object", "properties": {"user_id": {"type": "string"}}}
        }
    }
]

async def route_intent(user_message: str) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful assistant for an LMS. Use tools to answer user questions about labs, tasks, and student scores."},
        {"role": "user", "content": user_message}
    ]

    for _ in range(5):  # Max 5 reasoning steps
        resp = await llm_client.chat_completion(messages, tools=TOOLS)
        if not resp:
            return "Sorry, I'm having trouble thinking right now."

        choice = resp["choices"][0]["message"]
        messages.append(choice)

        if not choice.get("tool_calls"):
            return choice["content"]

        for tool_call in choice["tool_calls"]:
            func_name = tool_call["function"]["name"]
            args = json.loads(tool_call["function"]["content"] if "content" in tool_call["function"] else tool_call["function"]["arguments"])
            
            print(f"[tool] LLM called: {func_name}({args})", file=sys.stderr)
            
            try:
                if func_name == "get_items":
                    result = await lms_client.get_items()
                elif func_name == "get_pass_rates":
                    result = await lms_client.get_pass_rates(args.get("lab"))
                elif func_name == "get_learners":
                    result = await lms_client.get_learners()
                else:
                    result = f"Error: Tool {func_name} not implemented."
                
                print(f"[tool] Result: Received data", file=sys.stderr)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": json.dumps(result)
                })
            except Exception as e:
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": str(e)
                })

    return "I've thought too much about this. Please try a simpler question."
