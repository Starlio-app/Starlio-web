import http

import uvicorn
import yaml

from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from fastapi import FastAPI
from src.middleware.plausible_analytics import PlausibleAnalytics

config = yaml.safe_load(open('./config.yaml'))

from src.routes import index
from src.routes import wallpaper

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
