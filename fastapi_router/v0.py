import logging
from fastapi import APIRouter, Request, Response, BackgroundTasks
import json
import importlib
from fastapi.responses import JSONResponse
from database import mysql as db_mysql, session_helper
import time
import base64
import datetime
from tools import calculate
app_messages_verify = session_helper.Session("admin_app_messages_verify") #服务端发出的消息，服务端验证使用
app_messages_to_client = session_helper.Session("admin_app_messages_to_client") #服务端发出的消息，客户端验证使用
client_messages_verify = session_helper.Session("client_messages_verify") #客户端发出的消息，服务端验证使用
client_messages_to_app = session_helper.Session("client_messages_to_app") #客户端发出的消息，客户端验证使用

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
    res = {}
    # Check the return MD5 is correct
    easts = request.state.origin_data["east"]
    for east in easts:
        message_id = east["message_id"]
        app = east["application"]
        message = app_messages_to_client.get(".".join([user_id, app, message_id]))
        if message is None:
            continue
        message = message.decode('utf-8')
        if calculate.sha512_verify(".".join([message_id, user_id, app, message]), east["sign"]):
            app_messages_to_client.remove(".".join([user_id, app, message_id]))

    
    # Receive new messages from the client
    wests = request.state.origin_data["west"]
    data = {}
    for west in wests:
        try:
            message_id = west["message_id"]
            app = west["application"]
            destination = west["destination"]
            message = west["message"]
            if type(message) == dict or type(message) == list:
                message = calculate.base64_encode(json.dumps(message, indent=0))
            if client_messages_verify.get(".".join([destination, app, message_id])) is None:
                client_messages_verify.add(".".join([destination, app, message_id]), message)
                client_messages_to_app.add(".".join([destination, app, message_id]), message)
            sign = calculate.sha512(".".join(
            [message_id, destination, app, message]))
            data[message_id] = {
                "sign": sign,
                "application": app,
                "destination": destination,
            }
        except:
            import traceback
            logging.error(traceback.format_exc())
        

    # Send the return MD5 of the previous message to the client
    res["west"] = data

    # Send new messages to the client
    data = {}
    new_messages = app_messages_to_client.find(user_id)
    for new_message in new_messages:
        
        message = app_messages_to_client.get(new_message)
        message_id = new_message.split(".")[2]
        app = new_message.split(".")[1]
        destination = new_message.split(".")[0]
        if type(message) == bytes:
            message = message.decode('utf-8')
        data[message_id] = {
            "destination": destination,
            "message": message,
            "application": app
        }

    res["east"] = data

    return JSONResponse({"ret": 0, "msg": "successful", "data": res})