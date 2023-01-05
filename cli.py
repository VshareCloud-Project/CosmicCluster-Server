import sys
import argparse
import logging
from logging import handlers
import configloader
import importlib
c = configloader.config()
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
logging.getLogger('').addHandler(file_log_handler)
args = sys.argv[1:]
if len(args) > 2:
    if args[0] == "app":
        appname = args[1]
        logging.debug("Appname: " + appname)
        installed_apps = c.getkey("installed_apps")
        logging.debug("Installed apps: " + str(installed_apps))
        if appname in installed_apps:
            try:
                tclass = importlib.import_module("applications." + appname )
                
            except ImportError:
                import traceback
                logging.error("App not found")
                logging.error(traceback.format_exc())
                exit(1)
            tclass.cli_main(args[2:])
            exit(0)
        else:
            print("ERROR: App not installed")
            exit(1)
parser = argparse.ArgumentParser()
