from database import redis as redis_cli
import configloader
class Session():
    def __init__(self,namespace,default_expire=86400):
        self.c = configloader.config()
        self.r = redis_cli.newredis()
        self.default_expire = default_expire
        self.namespace = namespace
        self.redis_session_prefix = self.c.getkey("message_session_prefix")+"."+namespace

    def add(self,utag,value,expire=None):
        if expire == None:
            expire = self.default_expire
        redis_key = self.redis_session_prefix + "." + utag
        self.r.set(redis_key,value,ex=expire)

    def remove(self,utag):
        redis_key = self.redis_session_prefix + "." + utag
        self.r.delete(redis_key)

    def get(self,utag):
        redis_key = self.redis_session_prefix + "." + utag
        return self.r.get(redis_key)
        
    def find(self,attr):
        res = [str(i,"utf-8").replace(self.redis_session_prefix+".","") for i in self.r.keys(self.redis_session_prefix+"."+attr+".*")]
        return res
