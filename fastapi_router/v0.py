from fastapi import APIRouter, Request, Response, BackgroundTasks
import json
import importlib
from fastapi.responses import JSONResponse
router = APIRouter(
    prefix="/v0",
    responses={
        404: {
            "ret": 404,
            "msg": "Not found"
        },
        500: {
            "ret": 500,
            "msg": "Server error"
        },
        400: {
            "ret": 400,
            "msg": "Bad request"
        },
        401: {
            "ret": 401,
            "msg": "UnAuthorized"
        }
    })

@router.post("/ping")
async def post_ping(request:Request):
    return JSONResponse({"ret": 0, "msg": "pong"})