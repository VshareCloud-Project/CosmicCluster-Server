import pymysql
import configloader
import os
import sys
import logging

class db:

    def __init__(self,default_db="mysql"):
        c = configloader.config()
        self.dbname = default_db
        self.c = c
        self.d = pymysql.Connect(host=c.getkey(default_db)["host"], user=c.getkey(default_db)["user"], password=c.getkey(default_db)["password"], database=c.getkey(default_db)["database"])
        self.cursor = self.d.cursor()
    def __del__(self):
        self.d.close()
    def logcmd(self,command):
        need_log = self.c.getkey(self.dbname)["execute_log"]
        if need_log is True:
            logging.debug("execute command: %s",command)
        
    def read_cmd(self,command):
        try:
            self.logcmd(command)
            self.d.ping(reconnect=True)
            self.cursor.execute(command)
            res = self.cursor.fetchall()
            return res
        except pymysql.Error:
            import traceback
            logging.error(traceback.format_exc())
            return None
    def run_cmd(self,command):
        try:
            self.logcmd(command)
            self.d.ping(reconnect=True)
            self.cursor.execute(command)
            res = self.cursor.fetchall()
            # 提交到数据库执行
            self.d.commit()
        except pymysql.Error:
            # Rollback in case there is any error
            self.d.rollback()
            import traceback
            logging.error(traceback.format_exc())
            return False
        return res
    def run_multi_cmd(self,command):
        try:
            self.logcmd(command)
            self.d.ping(reconnect=True)
            self.cursor.execute(command)
        except pymysql.Error:
            # Rollback in case there is any error
            self.d.rollback()
            import traceback
            logging.error(traceback.format_exc())
            return False
        return True
    def commit(self):
        try:
            self.d.commit()
        except pymysql.Error:
            # Rollback in case there is any error
            self.d.rollback()
            import traceback
            logging.error(traceback.format_exc())
            return False