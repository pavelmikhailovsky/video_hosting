import logging

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter
from starlette.requests import Request
from starlette.responses import Response

from core.config import settings
from core.db import database
from src.users.api import users_app
from src.video.api import video_app


logging.basicConfig(level=logging.DEBUG, format='DateTime: %(asctime)s :: %(levelname)s :: Msg --> %(message)s')

app = FastAPI()

@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    response = Response('Internal server error', status_code=500)

    try:
        request.state.db = database()
        response = await call_next(request)
    finally:
        request.state.db.close()

    return response


routers = APIRouter(prefix=settings.API_V1_STR)
routers.include_router(video_app)
routers.include_router(users_app)

app.include_router(routers)


if __name__ == '__main__':
    load_dotenv()
    uvicorn.run('main:app', host=settings.HOST, port=settings.PORT, reload=True)
