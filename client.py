from utils import Utils
from Cryptodome import Random
from Cryptodome.Cipher import AES


class Client:
    def __init__(self):
        self.key = b'0123456789ABCDEF'  # get a Key in bytes
        self.iv = Random.new().read(AES.block_size)  # get an iv in bytes
        self.filePath = "ClientMassage.txt"  # file needs to be sent

    def encrpyt_message(self):
        file = open(self.filePath, "r")
        message = file.read()

        # 直接加密
        return Utils.aes_cbc_encrypt(self.iv, message, self.key)

        # 拆分AES-CBC加密
        # this function return ciphertext in bytes
        # encrypt_message = Utils.aes_cbc_encrypt_split(self.iv, message, self.key)
        # return encrypt_message

    def decrypt_message(self, message):
        # 直接解密
        # return Utils.aes_cbc_decrypt(self.iv, message, self.key)

        # 拆分AES-CBC解密
        # this function return plaintext in bytes
        decrypt_message = Utils.aes_cbc_decrypt_split(self.iv, message, self.key)
        return decrypt_message
