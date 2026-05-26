import uuid

from fastapi import Request, Response
from app.config.logger import logger

async def add_req_id(
        request: Request,
        call_next
):
    new_id = str(uuid.uuid4())    
    request.state.requestid = new_id

    message = (f"[{new_id}]" f"{request.method}" f"{request.url}")

    logger["middleware"].info(message)

    if request.method in logger:
        logger[request.method].info(message)

    response: Response = await call_next(request)

    response.headers["X-Request-ID"] = new_id


    return response