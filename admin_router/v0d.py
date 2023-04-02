# This file is deprecated and will be removed in the future
from fastapi import APIRouter, Request, Response, BackgroundTasks
import json
import importlib
from fastapi.responses import JSONResponse
from database import mysql as db_mysql
import time
import base64
import datetime

from tools.calculate import genuuid

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
    data = request.state.origin_data
    app = data["application"]
    app_task_id = data["task_id"]
    task_id = genuuid()
    func_name = data["function"]
    func_args = data["args"]
    cost_base = data["cost_base"]
    cost_magnification = data["cost_magnification"]
    if "cpu_arch" in data:
        cpu_arch = data["cpu_arch"]
    else:
        cpu_arch = "x86_64"
    if "rank_cpu" in data:
        rank_cpu = data["rank_cpu"]
    else:
        rank_cpu = 0
    if "rank_mem" in data:
        rank_mem = data["rank_mem"]
    else:
        rank_mem = 0
    if "rank_disk" in data:
        rank_disk = data["rank_disk"]
    else:
        rank_disk = 0
    if "step_target" in data:
        step_target = data["step_target"]
    else:
        step_target = 1
    add_time = datetime.datetime.now()
    db = db_mysql.db()
    db.run_cmd(
        """INSERT INTO `task` (
            `task_uuid`,
            `application`, 
            `app_task_uuid`, 
            `function_name`, 
            `args`, 
            `cost_base`, 
            `cost_magnification`, 
            `cpu_arch`, 
            `rank_cpu`, 
            `rank_mem`, 
            `rank_disk`, `
            step_target`,
            "add_time") 
            VALUES (
                "{task_id}",
                "{app}", 
                "{app_task_id}", 
                "{func_name}", 
                "{func_args}", 
                {cost_base}, 
                {cost_magnification}, 
                "{cpu_arch}", 
                {rank_cpu}, 
                {rank_mem}, 
                {rank_disk}, 
                {step_target},
                "{add_time}");""".format(
            task_id=task_id,
            app=app,
            app_task_id=app_task_id,
            func_name=func_name,
            func_args=func_args,
            cost_base=cost_base,
            cost_magnification=cost_magnification,
            cpu_arch=cpu_arch,
            rank_cpu=rank_cpu,
            rank_mem=rank_mem,
            rank_disk=rank_disk,
            step_target=step_target,
            add_time=add_time )
    )
    return JSONResponse({"ret": 0, "msg": "ok", "app_task_id": app_task_id, "task_id": task_id})  
    pass

@router.post("/gettask")
async def post_status(request: Request, backgroundtasks: BackgroundTasks):
    data = request.state.origin_data
    app = data["application"]
    app_task_id = data["task_id"]
    db = db_mysql.db()
    

@router.post("/addtasks")
async def post_addtasks(request: Request, backgroundtasks: BackgroundTasks):
    #TODO add multi tasks
    return JSONResponse({"ret": -1, "msg": "Future feature"})

@router.post("/gettasks")
async def post_gettasks(request: Request, backgroundtasks: BackgroundTasks):
    #TODO get multi tasks
    return JSONResponse({"ret": -1, "msg": "Future feature"})