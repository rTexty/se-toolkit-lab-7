import httpx
from bot.config import config


class LMSClient:
    def __init__(self):
        self.base_url = config.LMS_API_URL.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {config.LMS_API_KEY}",
            "Content-Type": "application/json",
        }

    async def get_items(self):
        """Fetch labs and tasks from /items/."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/items/",
                    headers=self.headers,
                    timeout=10.0,
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise Exception(
                    f"Backend error: HTTP {e.response.status_code} {e.response.reason_phrase}. "
                    "The backend service may be down."
                )
            except httpx.RequestError as e:
                raise Exception(f"Backend error: {str(e)}. Check that the services are running.")

    async def get_pass_rates(self, lab_id: str):
        """Fetch per-task pass rates for a specific lab."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/analytics/pass-rates",
                    params={"lab": lab_id},
                    headers=self.headers,
                    timeout=10.0,
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise Exception(f"Backend error: HTTP {e.response.status_code} {e.response.reason_phrase}.")
            except httpx.RequestError as e:
                raise Exception(f"Backend error: {str(e)}.")

    async def get_groups(self, lab_id: str):
        """Fetch per-group performance for a specific lab."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/analytics/groups",
                    params={"lab": lab_id},
                    headers=self.headers,
                    timeout=10.0,
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise Exception(f"Backend error: HTTP {e.response.status_code} {e.response.reason_phrase}.")
            except httpx.RequestError as e:
                raise Exception(f"Backend error: {str(e)}.")

    async def get_learners(self):
        """Fetch learners from /learners/."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/learners/",
                    headers=self.headers,
                    timeout=10.0,
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise Exception(f"Backend error: HTTP {e.response.status_code} {e.response.reason_phrase}.")
            except httpx.RequestError as e:
                raise Exception(f"Backend error: {str(e)}.")


lms_client = LMSClient()
