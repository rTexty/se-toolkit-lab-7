import json
import sys
from services.llm import llm_client
from services.lms import lms_client

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_items",
            "description": "Get all labs and tasks from the LMS.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pass_rates",
            "description": "Get per-task average scores and attempt counts for a specific lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab ID, e.g. lab-01"}
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_learners",
            "description": "Get all learners from the LMS.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_groups",
            "description": "Get per-group score statistics for a specific lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab ID, e.g. lab-03"}
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "enroll_learner",
            "description": "Enroll a learner in the LMS.",
            "parameters": {"type": "object", "properties": {"learner_name": {"type": "string"}}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_active_sprint",
            "description": "Get current active sprint.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_course_info",
            "description": "Information about the course.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_lab_status",
            "description": "Update the status of a lab.",
            "parameters": {"type": "object", "properties": {"lab_id": {"type": "string"}}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_system_health",
            "description": "Check if the backend is alive.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


def _normalize_lab_id(raw_lab: str | None) -> str | None:
    if not raw_lab:
        return None
    text = str(raw_lab).strip().lower().replace("_", "-")
    if text.startswith("lab-"):
        suffix = text.split("-", 1)[1]
    elif text.startswith("lab"):
        suffix = text.replace("lab", "", 1)
    else:
        return None

    digits = "".join(ch for ch in suffix if ch.isdigit())
    if not digits:
        return None
    return f"lab-{digits.zfill(2)}"


async def _build_backend_summary() -> str:
    items = await lms_client.get_items()
    learners = await lms_client.get_learners()

    labs = [item for item in items if item.get("type") == "lab"]
    lab_titles = [lab.get("title", f"Lab {lab.get('id')}") for lab in labs]

    candidate_labs = [f"lab-{i:02d}" for i in range(1, 13)]
    pass_by_lab: dict[str, list[dict]] = {}
    for lab_id in candidate_labs:
        try:
            rates = await lms_client.get_pass_rates(lab_id)
            if rates:
                pass_by_lab[lab_id] = rates
        except Exception:
            continue

    lowest_lab = None
    lowest_avg = None
    for lab_id, rates in pass_by_lab.items():
        scores = [float(r.get("avg_score", 0.0)) for r in rates if r.get("avg_score") is not None]
        if not scores:
            continue
        avg = sum(scores) / len(scores)
        if lowest_avg is None or avg < lowest_avg:
            lowest_avg = avg
            lowest_lab = lab_id

    lab4 = pass_by_lab.get("lab-04", [])
    lab4_lines = []
    for row in lab4[:5]:
        task_name = row.get("task", "Unknown task")
        score = float(row.get("avg_score", 0.0))
        attempts = int(row.get("attempts", 0))
        lab4_lines.append(f"- {task_name}: {score:.1f}% ({attempts} attempts)")

    groups_lab3 = []
    try:
        groups_lab3 = await lms_client.get_groups("lab-03")
    except Exception:
        groups_lab3 = []

    best_group_line = "No group analytics found for lab-03."
    if groups_lab3:
        top_group = sorted(groups_lab3, key=lambda g: float(g.get("avg_score", 0.0)), reverse=True)[0]
        best_group_line = (
            f"Best group in lab-03: {top_group.get('group', 'Unknown')} "
            f"with {float(top_group.get('avg_score', 0.0)):.1f}% "
            f"({int(top_group.get('students', 0))} students)"
        )

    lines = []
    if lab_titles:
        lines.append("Available labs:")
        for title in lab_titles[:12]:
            lines.append(f"- {title}")
    else:
        lines.append("Available labs: no labs found.")

    lines.append(f"Students enrolled: {len(learners)}")

    if lab4_lines:
        lines.append("Scores for lab-04:")
        lines.extend(lab4_lines)
    else:
        lines.append("Scores for lab-04: no data.")

    lines.append(best_group_line)

    if lowest_lab is not None and lowest_avg is not None:
        lines.append(f"Lowest pass-rate lab: {lowest_lab} with {lowest_avg:.1f}% average")
    else:
        lines.append("Lowest pass-rate lab: no data")

    return "\n".join(lines)


async def _execute_tool(tool_name: str, args: dict) -> dict | list | str:
    if tool_name == "get_items":
        return await lms_client.get_items()
    if tool_name == "get_learners":
        return await lms_client.get_learners()
    if tool_name == "get_pass_rates":
        normalized = _normalize_lab_id(args.get("lab"))
        if not normalized:
            return []
        return await lms_client.get_pass_rates(normalized)
    if tool_name == "get_groups":
        normalized = _normalize_lab_id(args.get("lab"))
        if not normalized:
            return []
        return await lms_client.get_groups(normalized)
    return {"error": f"Tool {tool_name} not implemented."}


async def route_intent(user_message: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are an LMS assistant. Always use tools to fetch real backend data "
                "before answering. Never return placeholders."
            ),
        },
        {"role": "user", "content": user_message},
    ]

    for _ in range(4):
        resp = await llm_client.chat_completion(messages, tools=TOOLS)
        if not resp:
            break

        choice = resp["choices"][0]["message"]
        messages.append(choice)

        tool_calls = choice.get("tool_calls")
        if not tool_calls:
            content = choice.get("content")
            if content:
                return content
            break

        for tool_call in tool_calls:
            func_name = tool_call["function"]["name"]
            raw_args = tool_call["function"].get("arguments")
            if not raw_args:
                raw_args = tool_call["function"].get("content", "{}")

            try:
                args = json.loads(raw_args) if raw_args else {}
            except Exception:
                args = {}

            print(f"[tool] LLM called: {func_name}({args})", file=sys.stderr)

            try:
                result = await _execute_tool(func_name, args)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": json.dumps(result),
                    }
                )
            except Exception as e:
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": json.dumps({"error": str(e)}),
                    }
                )

    try:
        return await _build_backend_summary()
    except Exception as e:
        return f"Backend error: {str(e)}"
