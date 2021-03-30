from utils import Utils
from Cryptodome import Random
from Cryptodome.Cipher import AES


class Client:
    def __init__(self):
        self.Key = '0123456789ABCDEF'.encode()
        self.iv = Random.new().read(AES.block_size)
        self.filePath = "ClientMassage.txt"

    def encrpyt_message(self):
        file = open(self.filePath, "r")
        message = file.read()
        encrypt_message = Utils.aes_cbc_encrypt(str(self.iv) + message, self.Key)
        return encrypt_message[16:]

