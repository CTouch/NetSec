from utils import Utils
from Cryptodome import Random
from Cryptodome.Cipher import AES
from mpc import Mpc
import random


class Client:
    def __init__(self, mpc):
        self.key = b'0123456789ABCDEF'  # get a Key in bytes
        self.iv = Random.new().read(AES.block_size)  # get an iv in bytes
        self.filePath = "ClientMassage.txt"  # file needs to be sent
        self.mpc = mpc

    def start(self):
        print("How do you set your Message : 1->terminal input 2->file ")
        message = ''
        number = input()
        if number == '1':
            print("Please enter the Message :")
            message = input()
        elif number == '2':
            print("Please enter the file path :")
            c = input()
            if c != '':
                self.filePath = input()
            else:
                print("Then we use default file")
            try:
                file = open(self.filePath, "r")
                message = file.read()
            except Exception as r:
                print('error: %s' % r)
                return
        else:
            print("error")
        k = len(message)
        c = random.randint(1, k)
        if isinstance(self.mpc, Mpc):
            print("client is ready for MPC ")
            self.mpc.set_message_client(self.iv, message[:c], message[c:], self.key)
        else:
            print("error! ")

    # def check_info(self, message):
    #     lines = []
    #     while True:
    #         try:
    #             lines.append(input('end with CTRL+D \n'))
    #         except:
    #             break
    #     print(lines)

    # def encrpyt_message(self):
    #     file = open(self.filePath, "r")
    #     message = file.read()
    #
    #     # 直接加密
    #     return Utils.aes_cbc_encrypt(self.iv, message, self.key)
    #
    #     # 拆分AES-CBC加密
    #     # this function return ciphertext in bytes
    #     # encrypt_message = Utils.aes_cbc_encrypt_split(self.iv, message, self.key)
    #     # return encrypt_message
    #
    # def decrypt_message(self, message):
    #     # 直接解密
    #     # return Utils.aes_cbc_decrypt(self.iv, message, self.key)
    #
    #     # 拆分AES-CBC解密
    #     # this function return plaintext in bytes
    #     decrypt_message = Utils.aes_cbc_decrypt_split(self.iv, message, self.key)
    #     return decrypt_message
