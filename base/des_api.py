import time
from datetime import datetime
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
import binascii

# 固定 DES 密钥（Java 中会自动截断到 8 字节）
KEY = b"sgEsmU8F"  # 注意：原始字符串前 8 字节

def des_encrypt_ecb(plaintext: str) -> str:
    """
    DES ECB 模式加密，PKCS#5 填充，输出 hex 小写字符串
    :param plaintext: 明文字符串
    :return: 十六进制表示的密文
    """
    cipher = DES.new(KEY, DES.MODE_ECB)
    # UTF-8 编码明文
    plaintext_bytes = plaintext.encode('utf-8')
    # PKCS#5 填充（块大小 8 字节）
    padded_text = pad(plaintext_bytes, DES.block_size)
    # 加密
    encrypted = cipher.encrypt(padded_text)
    # 返回小写 hex 字符串
    return binascii.hexlify(encrypted).decode('utf-8')

def des_decrypt_ecb(hex_ciphertext: str) -> str:
    """
    DES ECB 解密（用于验证）
    :param hex_ciphertext: 十六进制密文字符串
    :return: 明文字符串
    """
    cipher = DES.new(KEY, DES.MODE_ECB)
    ciphertext = binascii.unhexlify(hex_ciphertext)
    padded_plaintext = cipher.decrypt(ciphertext)
    # 去除 PKCS#5 填充
    plaintext = pad.remove_pad(padded_plaintext, DES.block_size)
    return plaintext.decode('utf-8')

# main 函数模拟
if __name__ == "__main__":
    timestamp = int(time.time() * 1000)  # 毫秒时间戳
    plaintext = f"aa@{timestamp}"
    encrypted = des_encrypt_ecb(plaintext)
    print(encrypted)

    # 可选：测试解密
    # decrypted = des_decrypt_ecb(encrypted)
    # print("Decrypted:", decrypted)