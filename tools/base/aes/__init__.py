from Crypto.Cipher import AES  # 需要安装 pycryptodome 或者 pycrypto
import base64
from functools import reduce
import random
from string import digits, ascii_letters, punctuation
import uuid
def genpassword(length=16)->str:
    """
    生成随机hex密码
    """
    return uuid.uuid4().hex
def hextobytes(hexstr: str)->bytes:
    """
    将 hex 转换为 bytes
    """
    return bytes.fromhex(hexstr)
def bytestohex(data: bytes)->str:
    """
    将 bytes 转换为 hex
    """
    return data.hex()
def cbc_encrypt(data: bytes, key: str)->str:
    """
    AES-CBC 加密
    key 必须是 16(AES-128)、24(AES-192) 或 32(AES-256) 字节的 AES 密钥；
    初始化向量 iv 为随机的 16 位字符串 (必须是16位)，
    解密需要用到这个相同的 iv，因此将它包含在密文的开头。
    """
    block_size = len(key)
    data = base64.b64encode(data).decode(encoding='utf-8')
    padding = (block_size - len(data) % block_size) or block_size  # 填充字节
    iv = reduce(lambda x, y: x + random.choice(digits + ascii_letters + punctuation), range(16), "")
    mode = AES.new(hextobytes(key), AES.MODE_CBC, iv.encode())
    ciphertext = mode.encrypt((data + padding * chr(padding)).encode())
    return base64.b64encode(iv.encode() + ciphertext).decode()

def cbc_decrypt(ciphertext: str, key: str)->bytes:
    """
    AES-CBC 解密
    密文的前 16 个字节为 iv
    """
    ciphertext = base64.b64decode(ciphertext)
    mode = AES.new(hextobytes(key), AES.MODE_CBC, ciphertext[:AES.block_size])
    plaintext = mode.decrypt(ciphertext[AES.block_size:]).decode()
    return base64.b64decode(plaintext[:-ord(plaintext[-1])])