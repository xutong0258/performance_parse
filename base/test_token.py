import time
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def generate_token(username: str) -> str:
    """
    生成 token：username@13位时间戳，AES-192-ECB 加密，Base64 编码
    """
    # 1. 构造明文：username@13位时间戳（毫秒）
    timestamp = int(time.time() * 1000)  # 13位时间戳
    plaintext = f"{username}@{timestamp}"
    
    # 2. 密钥（24字节，用于AES-192）
    key = "sgEsmU8FdP8W7j5H03695286".encode('utf-8')  # 24 bytes
    
    # 3. 确保密钥长度正确（AES-192 需要 24 字节）
    if len(key) != 24:
        raise ValueError("密钥长度必须为24字节（AES-192）")
    
    # 4. 使用 AES-192-ECB 加密
    cipher = AES.new(key, AES.MODE_ECB)
    
    # 5. 对明文进行 PKCS7 填充，并加密
    padded_data = pad(plaintext.encode('utf-8'), AES.block_size)
    encrypted_bytes = cipher.encrypt(padded_data)
    
    # 6. Base64 编码为字符串
    token = base64.b64encode(encrypted_bytes).decode('utf-8')
    
    return token

# 示例使用
if __name__ == "__main__":
    username = "alice"
    token = generate_token(username)
    print("Generated token:", token)