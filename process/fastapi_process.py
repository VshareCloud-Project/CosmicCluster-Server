import imp
import threading
import fastapi
import uvicorn
import os
import base64
import logging
import configloader
import json
from database import mysql as db_mysql
import fastapi_router.v0 as v0_router
from tools.base import aes
from tools.base.rsa_utils import openssl as rsa
from fastapi import Response
from fastapi.responses import JSONResponse
class fastapi_process(threading.Thread):
    '''
    The FastAPI Process
    '''
    def __init__(self,bind="0.0.0.0",bind_port=80):
        super().__init__()
        self.bind = bind
        self.c = configloader.config()
        self.bind_port = bind_port
        self.fastapi = fastapi.FastAPI()
        fp = open(self.c.getkey("rsa_private_key"),"rb")
        self.private_key = fp.read()
        fp.close()
        fp = open(self.c.getkey("rsa_public_key"),"rb")
        self.public_key = fp.read()
        fp.close()
        @self.fastapi.middleware("http")
        async def auth_v0(request: fastapi.Request, call_next):
            try:
                    decrypt_rsa_class = rsa.rsa_utils(prikey=self.private_key,pubkey=self.public_key)
                    encrypted_data_raw = await request.body()
                    request.state.origin_data_raw = encrypted_data_raw
                    encrypted_data_dict = json.loads(encrypted_data_raw)
                    encrypted_data = encrypted_data_dict["encrypt"]
                    user_id = encrypted_data_dict["user_id"]
                    encrypted_token = base64.b64decode(encrypted_data_dict["token"])
                    try:
                        encrypted_token_decrypt1 = decrypt_rsa_class.decrypt(encrypted_token)
                    except:
                        return Response({"ret":400,"msg":"Decrypt Failed"},status_code=400)
                    db = db_mysql.db()
                    db_res = db.read_cmd("SELECT keychain FROM `dnode` WHERE `uuid` = \"%s\""% (user_id,))
                    if len(db_res) == 0:
                        return Response({"ret":400,"msg":"User Not Found!"},status_code=400)
                    keychain = db_res[0][0].encode()
                    encrypted_sign = base64.b64decode(encrypted_data_dict["sign"])
                    sign_rsa_class = rsa.rsa_utils(pubkey=keychain)
                    try:
                        assert sign_rsa_class.verify(encrypted_data.encode(),encrypted_sign) == True
                    except:
                        return Response({"ret":400,"msg":"User Verify failed"},status_code=400)
                    
                    
                    try:
                        encrypted_data_decrypt = aes.cbc_decrypt(encrypted_data,encrypted_token_decrypt1.decode())
                    except:
                        return Response({"ret":400,"msg":"Decrypt Failed"},status_code=400)
                    org_data = json.loads(encrypted_data_decrypt)
                    request.state.origin_data = org_data
            except:
                import traceback
                logging.error(traceback.format_exc())
                return Response("Verify Failed",status_code=400)
            response = await call_next(request)
            if response.status_code == 200:
                response_body = b""
                async for chunk in response.body_iterator:
                    response_body += chunk
                newpassword = aes.genpassword(32)
                new_response_body={}
                new_response_body["encrypt"] = aes.cbc_encrypt(response_body,newpassword)
                new_response_body["sign"] = base64.b64encode(decrypt_rsa_class.sign(new_response_body["encrypt"].encode())).decode()
                new_response_body["token"] = base64.b64encode(sign_rsa_class.encrypt(newpassword.encode())).decode()
                response = JSONResponse(new_response_body)

            return response
        self.fastapi.include_router(v0_router.router)
    def run(self):
        uvicorn.run(self.fastapi,host=self.bind,port=self.bind_port)