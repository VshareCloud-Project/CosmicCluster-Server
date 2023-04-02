import os
import sys
from process import fastapi_process, adminapi_process
import configloader
import logging
from logging import handlers
from threading import Event
import ctypes
import inspect

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    try:
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            # pass
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    except Exception as err:
        print(err)

def _stop_thread(thread):
    """终止-线程"""
    _async_raise(thread.ident, SystemExit)

def main():
    c = configloader.config()
    event = Event()
    logging.basicConfig(
        level=getattr(logging,c.getkey("log_level")), format="%(asctime)s [%(levelname)s][%(pathname)s:%(lineno)d]: %(message)s"
    )
    if c.getkey("log_file") != "" and c.getkey("log_file") is not None:
        file_log_handler = handlers.RotatingFileHandler(c.getkey("log_file"), mode="a", encoding=c.getkey("log_file_encoding"), maxBytes=c.getkey("log_file_size"), backupCount=c.getkey("log_file_backup_count"))
        formatter = logging.Formatter("%(asctime)s [%(levelname)s][%(pathname)s:%(lineno)d]: %(message)s")
        file_log_handler.setFormatter(formatter)
        file_log_handler.setLevel(getattr(logging,c.getkey("log_level")))
        logging.getLogger('').addHandler(file_log_handler)
    if c.getkey("log_error_file") != "" and c.getkey("log_error_file") is not None:
        file_error_handler = handlers.RotatingFileHandler(c.getkey("log_error_file"), mode="a", encoding=c.getkey("log_file_encoding"), maxBytes=c.getkey("log_file_size"), backupCount=c.getkey("log_file_backup_count"))
        formatter = logging.Formatter("%(asctime)s [%(levelname)s][%(pathname)s:%(lineno)d]: %(message)s")
        file_error_handler.setFormatter(formatter)
        file_error_handler.setLevel(getattr(logging,c.getkey("log_error_level")))
        logging.getLogger('').addHandler(file_error_handler)
    logging.info("Starting process")
    p = fastapi_process.fastapi_process(c.getkey("bind"),c.getkey("port"))
    q = adminapi_process.adminapi_process(c.getkey("admin_bind"),c.getkey("admin_port"))
    q.start()
    p.start()
    while(p.is_alive()):
        try:
            if not q.is_alive():
                logging.error("AdminAPI process is dead, restarting")
                q.start()
            p.join(10)
        except (KeyboardInterrupt, SystemExit, SystemError):
            break
        except:
            import traceback
            logging.error("Error in main thread")
            logging.error(traceback.format_exc())
    if p.is_alive():
        _stop_thread(p)
        logging.info("Force Stopping process")
    if q.is_alive():
        _stop_thread(q)
        logging.info("Force Stopping process")
    return 0

if __name__ == "__main__":
    main()