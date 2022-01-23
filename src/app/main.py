from fastapi import FastAPI
from src.app.api.routes.router import api_router
from src.app.config import (API_PREFIX, APP_NAME, APP_VERSION,
                            IS_DEBUG)
from src.app.core.event_handlers import (start_app_handler,
                                         stop_app_handler)
from starlette.responses import RedirectResponse
import ptvsd
import os
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


def get_app() -> FastAPI:

    fast_app = FastAPI(title=APP_NAME, version=APP_VERSION, debug=IS_DEBUG)
    fast_app.include_router(api_router, prefix=API_PREFIX)
    fast_app.add_middleware(
        DBSessionMiddleware,
        db_url=os.environ.get("DATABASE_URI"),
    )

    fast_app.add_event_handler("startup", start_app_handler(fast_app))
    fast_app.add_event_handler("shutdown", stop_app_handler(fast_app))

    return fast_app


app = get_app()

ptvsd.enable_attach(address=('0.0.0.0', 5678))

@app.get("/")
def main():
    return RedirectResponse(url="/docs/")
