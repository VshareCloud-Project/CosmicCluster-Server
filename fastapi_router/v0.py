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


@router.post("/gettask")
async def post_status(request: Request, backgroundtasks: BackgroundTasks):
    node_status_data = request.state.origin_data["status"]
    user_id = request.state.user_uuid
    db = db_mysql.db()
    db.run_multi_cmd(
        """UPDATE `dnode` SET `cpus` = {cpu_num},`memory` = {memory_total},`storage` = {hdd_all_total},`disk_info` = "{disk_info}", `last_seen`="{last_seen}" WHERE `uuid` = "{user_id}";
    """.format(cpu_num=node_status_data["cpu_num"],
               memory_total=node_status_data["memory_total"],
               hdd_all_total=node_status_data["hdd_all_total"],
               disk_info=base64.b64encode(
                   json.dumps(node_status_data["disk_info"]).encode()).decode("utf-8"),
               last_seen=datetime.datetime.now(),
               user_id=user_id,
               percent_cpu=node_status_data["cpu_persent"] / 100,
               percent_mem=node_status_data["memory_used"] / node_status_data["memory_total"],
               percent_disk=node_status_data["hdd_all_used"] / node_status_data["hdd_all_total"]))
    db.run_cmd(
        """INSERT INTO `dnode_status_log` (`node_id`, `percent_cpu`,`percent_mem`,`percent_disk`,`disk_info`,`update_time`) VALUES ("{user_id}", {percent_cpu},{percent_mem}, {percent_disk},"{disk_info}","{last_seen}");
""".format(cpu_num=node_status_data["cpu_num"],
           memory_total=node_status_data["memory_total"],
           hdd_all_total=node_status_data["hdd_all_total"],
           disk_info=base64.b64encode(json.dumps(
               node_status_data["disk_info"]).encode()).decode("utf-8"),
           last_seen=datetime.datetime.now(),
           user_id=user_id,
           percent_cpu=node_status_data["cpu_persent"] / 100,
           percent_mem=node_status_data["memory_used"] / node_status_data["memory_total"],
           percent_disk=node_status_data["hdd_all_used"] / node_status_data["hdd_all_total"]))
    tasks = request.state.origin_data["tasks"]
    checks = request.state.origin_data["check"]
    for check in checks:
        pass
        #TODO: Check the task
    for taskid,task in tasks.items():
        backgroundtasks.add_task(task["task"],taskid,task["data"])
        #TODO: Hold on the task
    return JSONResponse({"ret": 0, "msg": "successful"})