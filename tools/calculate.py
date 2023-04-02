import uuid
import base64

def genuuid():
    return str(uuid.uuid4())

def base64_encode(string:str)->str:
    return base64.b64encode(string.encode('utf-8')).decode('utf-8')

def base64_decode(string:str)->str:
    return base64.b64decode(string.encode('utf-8')).decode('utf-8')

def base64_encode_bytes(string:bytes)->str:
    return base64.b64encode(string).decode('utf-8')

def base64_decode_bytes(string:str)->bytes:
    return base64.b64decode(string.encode('utf-8'))

def sha512(string:str)->str:
    import hashlib
    return hashlib.sha512(string.encode('utf-8')).hexdigest()

def sha512_verify(string:str, sign:str)->bool:
    import hashlib
    return hashlib.sha512(string.encode('utf-8')).hexdigest() == sign

def sha384(string:str)->str:
    import hashlib
    return hashlib.sha384(string.encode('utf-8')).hexdigest()

def sha384_verify(string:str, sign:str)->bool:
    import hashlib
    return hashlib.sha384(string.encode('utf-8')).hexdigest() == sign

def sha256(string:str)->str:
    import hashlib
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

def sha256_verify(string:str, sign:str)->bool:
    import hashlib
    return hashlib.sha256(string.encode('utf-8')).hexdigest() == sign

def md5(string:str)->str:
    import hashlib
    return hashlib.md5(string.encode('utf-8')).hexdigest()

def md5_verify(string:str, sign:str)->bool:
    import hashlib
    return hashlib.md5(string.encode('utf-8')).hexdigest() == sign

def hextobase64(string:str)->str:
    return base64.b64encode(bytes.fromhex(string)).decode('utf-8')

def base64tohex(string:str)->str:
    return base64.b64decode(string).hex()