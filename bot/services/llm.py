import httpx
import json
import sys
from bot.config import config

class LLMClient:
    def __init__(self):
        self.base_url = os.getenv("LLM_API_BASE_URL", "http://localhost:42005/v1")
        self.api_key = os.getenv("LLM_API_KEY", "placeholder_key")
        self.model = os.getenv("LLM_API_MODEL", "qwen-max")

    async def chat_completion(self, messages, tools=None):
        async with httpx.AsyncClient() as client:
            payload = {
                "model": self.model,
                "messages": messages,
            }
            if tools:
                payload["tools"] = tools
                payload["tool_choice"] = "auto"
            
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json=payload,
                    timeout=60.0
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"[LLM Error] {str(e)}", file=sys.stderr)
                return None

llm_client = LLMClient()
