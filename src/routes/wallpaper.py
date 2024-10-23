from http import HTTPStatus

import requests
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

template = Jinja2Templates(directory='./src/web/html')


@router.get('/wallpaper/today', response_class=HTMLResponse)
async def today_wallpaper(request: Request):
    res = requests.get(f'https://api.starlio.space/last')

    if HTTPStatus(res.status_code).is_server_error or HTTPStatus(res.status_code).is_client_error:
        return FileResponse('../web/html/error/404.html', status_code=HTTPStatus.NOT_FOUND)

    return template.TemplateResponse(
        request,
        '/wallpaper.html',
        {'info': res.json()}
    )


@router.get('/wallpaper/{day}', response_class=HTMLResponse)
async def wallpaper(request: Request, day):
    res = requests.get(f'https://api.starlio.space/wallpaper/{day}')

    if (HTTPStatus(res.status_code).is_server_error
            or HTTPStatus(res.status_code).is_client_error
            or len(res.json()) <= 0):

        return FileResponse('./src/web/html/error/404.html', status_code=HTTPStatus.NOT_FOUND)

    return template.TemplateResponse(
        request,
        '/wallpaper.html',
        {'info': res.json()}
    )
