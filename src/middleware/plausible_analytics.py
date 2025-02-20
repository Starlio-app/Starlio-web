"""
This module contains the PlausibleAnalytics middleware 
for sending analytics events
to Plausible Analytics after processing each request.

The middleware collects information about the request, 
such as the HTTP method, status code,
user agent, and source, and sends this data to the Plausible Analytics API.

In case of any client-side or server-side errors, no event is sent, 
and the response is returned as usual.
"""

from http import HTTPStatus

import yaml
import httpx
from user_agents import parse as ua_parse

config = yaml.safe_load(open('./config.yaml'))

class PlausibleAnalytics:
    """
    Middleware for sending analytics data to Plausible Analytics
    after processing each request.
    """
    
    async def __call__(self, request, call_next):
        """
        Called for each request, sends an event to Plausible with
        information about the request and user.

        Args:
            request: FastAPI request object.
            call_next: Function to call the next request handler.

        Returns:
            Response: FastAPI response object.
        """
        
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
                "browser": f"{user_agent_parsed.browser.family}" \
                f"{user_agent_parsed.browser.version_string}",
                "os": f"{user_agent_parsed.os.family}" \
                f"{user_agent_parsed.os.version_string}",
                "source": request.headers.get('referer', 'direct'),
            },
        }

        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    config['analytics']['endpoint'],
                    json=event,
                    headers={
                        "Authorization": f"Bearer {config['analytics']['token']}",
                        "Content-Type": "application/json",
                        "User-Agent": user_agent,
                    },
                )
        except Exception as e:
            print(f"Error sending event to Plausible: {e}")

        return response
