from Cryptodome.Cipher import AES
from Cryptodome import Random
import re

class Client:
    def __init__(self):
        self.Key = '0123456789ABCDEF'.encode()
        self.iv = Random.new().read(AES.block_size)
        self.filePath = "ClientMassage.txt"

    def encrpytMess(self):
        iv = self.iv
        key = self.Key
        encrpytMessage = iv
        file = open(self.filePath, "r")
        message = file.read()
        message = self.add_16(message)
        messageList = re.findall(r'.{16}', message)
        for M in messageList:
            aes = AES.new(key,AES.MODE_CBC,iv)
            cipherText = aes.encrypt(M.encode())
            iv = (iv.encode() ^ cipherText).decode()
            encrpytMessage += cipherText
        return encrpytMessage

    def add_16(self,data):
        tmp = data + '!' * (16 - (len(data)) % 16)
        # print(len(tmp))
        return tmp

