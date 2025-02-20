"""
This module contains routes for serving wallpapers using FastAPI.

Routes:
- `/wallpaper/today`: Fetches the wallpaper of the day 
and renders it using a template.
- `/wallpaper/{day}`: Fetches a specific wallpaper by day 
and renders it using a template.

In case of any client or server errors or empty data, 
a 404 error page is returned.
"""

from http import HTTPStatus

import requests
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

template = Jinja2Templates(directory='./src/web/html')


@router.get('/wallpaper/today', response_class=HTMLResponse)
async def today_wallpaper(request: Request):
    """
    Fetches the wallpaper of the day and renders it using a template.
    Returns a 404 page in case of client or server errors.

    Args:
        request: The FastAPI request object.

    Returns:
        HTMLResponse: The wallpaper page or 404 error page.
    """
    res = requests.get('https://api.starlio.space/last', timeout=3)

    if (HTTPStatus(res.status_code).is_server_error
    or HTTPStatus(res.status_code).is_client_error):
        return FileResponse(
            '../web/html/error/404.html', 
            status_code=HTTPStatus.NOT_FOUND
            )

    return template.TemplateResponse(
        request,
        '/wallpaper.html',
        {'info': res.json()}
    )


@router.get('/wallpaper/{day}', response_class=HTMLResponse)
async def wallpaper(request: Request, day):
    """
    Fetches a specific wallpaper by day and renders it using a template.
    Returns a 404 page in case of client or server errors \
    or if the wallpaper data is empty.

    Args:
        request: The FastAPI request object.
        day: The day parameter used to fetch the wallpaper.

    Returns:
        HTMLResponse: The wallpaper page or 404 error page.
    """
    res = requests.get('https://api.starlio.space/wallpaper/{day}', timeout=3)

    if (HTTPStatus(res.status_code).is_server_error
            or HTTPStatus(res.status_code).is_client_error
            or len(res.json()) <= 0):

        return FileResponse(
            './src/web/html/error/404.html', 
            status_code=HTTPStatus.NOT_FOUND
            )

    return template.TemplateResponse(
        request,
        '/wallpaper.html',
        {'info': res.json()}
    )
