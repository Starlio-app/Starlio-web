"""
This module defines the main FastAPI application, including route handlers,
middleware, static file serving, and error handling.

Routes:
- `/app-ads.txt`: Serves the `app-ads.txt` file.
- `/robots.txt`: Serves the `robots.txt` file.
- `/wallpaper/today`: Served by the wallpaper router, fetches today's wallpaper.
- `/wallpaper/{day}`: Served by the wallpaper router, fetches the wallpaper for a specific day.
"""

import http

import uvicorn
import yaml
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from src.middleware.plausible_analytics import PlausibleAnalytics
from src.routes import index, wallpaper

config = yaml.safe_load(open('config.yaml'))

app = FastAPI()

if config['analytics']['token']:
    app.middleware('http')(PlausibleAnalytics())

app.include_router(index.router)
app.include_router(wallpaper.router)

app.mount('/static/', StaticFiles(directory='./src/web/static/'))
app.mount('/.well-known/', StaticFiles(directory='./.well-known/'))


@app.get('/app-ads.txt')
async def app_ads():
    return FileResponse('./app-ads.txt')


@app.get('/robots.txt')
async def robots_txt():
    return FileResponse('./robots.txt')


@app.exception_handler(404)
async def not_found(req, __):
    return FileResponse('./src/web/html/error/404.html', status_code=http.HTTPStatus.NOT_FOUND)

if __name__ == '__main__':
    uvicorn.run(app,
                host=config['server']['host'],
                port=8000,
                ssl_keyfile=config['server']['ssl_privkey']
                if config['server']['ssl_work']
                else None,
                ssl_certfile=config['server']['ssl_cert']
                if config['server']['ssl_work']
                else None
                )
