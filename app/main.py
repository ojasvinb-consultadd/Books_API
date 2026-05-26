from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.api import router
from app.middleware.requestid import add_req_id
from app.config.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger["app"].info("database initialized")

    yield

    logger["app"].info("app shutting down")

    


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def req_id_middleware(request, call_next):
    return await add_req_id(request,call_next)

app.include_router(router)



