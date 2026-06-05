from fastapi import FastAPI
from api import router

def get_app():
    app = FastAPI()
    app.include_router(router=router)
    return app

app = get_app()