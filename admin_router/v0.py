from fastapi import APIRouter, Request, Response, BackgroundTasks
import json
import importlib
from fastapi.responses import JSONResponse
from database import mysql as db_mysql
import time
import base64
import datetime

router = APIRouter(prefix="/v0",
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
async def post_ping(request: Request):
    return JSONResponse({"ret": 0, "msg": "pong"})

@router.post("/addtask")
async def post_addtask(request: Request, backgroundtasks: BackgroundTasks):
    #TODO add task
    pass

@router.post("/gettask")
async def post_status(request: Request, backgroundtasks: BackgroundTasks):
    #TODO get task
    pass

@router.post("/addtasks")
async def post_addtasks(request: Request, backgroundtasks: BackgroundTasks):
    #TODO add multi tasks
    return JSONResponse({"ret": -1, "msg": "Future feature"})

@router.post("/gettasks")
async def post_gettasks(request: Request, backgroundtasks: BackgroundTasks):
    #TODO get multi tasks
    return JSONResponse({"ret": -1, "msg": "Future feature"})