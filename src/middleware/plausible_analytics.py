import httpx
import yaml

from http import HTTPStatus
from user_agents import parse as ua_parse

config = yaml.safe_load(open('./config.yaml'))

class PlausibleAnalytics:
    async def __call__(self, request, call_next):
        response = await call_next(request)

        user_agent = request.headers.get('user-agent', 'unknown')
        user_agent_parsed = ua_parse(user_agent)

        if HTTPStatus(response.status_code).is_client_error:
            return response

        event = {
            "domain": config['analytics']['domain'],
            "name": request.url.path or '404 - Not Found',
            "url": str(request.url),
            "props": {
                "method": request.method,
                "statusCode": response.status_code,
                "browser": f"{user_agent_parsed.browser.family} {user_agent_parsed.browser.version_string}",
                "os": f"{user_agent_parsed.os.family} {user_agent_parsed.os.version_string}",
                "source": request.headers.get('referer', 'direct'),
            },
        }

        async with httpx.AsyncClient() as client:
            try:
                await client.post(
                    config['analytics']['endpoint'],
                    json=event,
                    headers={
                        "Authorization": f"Bearer {config['analytics']['token']}",
                        "Content-Type": "application/json",
                        "User-Agent": request.headers.get('user-agent', 'unknown'),
                    },
                )
            except Exception as e:
                print(f"Error sending event to Plausible: {e}")

        return response