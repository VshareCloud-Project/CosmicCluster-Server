import redis
import configloader

def newredis():
    c = configloader.config()
    redis_conf = c.getkey("redis")
    if not "cluster" in redis_conf:
            r = redis.StrictRedis(
                host=redis_conf["host"],
                port=redis_conf["port"],
                db=redis_conf["db"],
                password=redis_conf["password"]
            )
            return r
