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
        self.split = 0
        self.message = ''

    #
    # def setMessagePath(self, filePath):
    #     self.filePath = filePath
    #
    # def __setattr__(self, key, value):

    def start(self):
        print("How do you set your Message : 1->terminal input 2->file ")
        self.message = ''
        number = input()
        if number == '1':
            print("Please enter the Message :")
            self.message = input()
        elif number == '2':
            print("Please enter the file path :")
            c = input()
            if c != '':
                self.filePath = input()
            else:
                print("Then we use default file")
            try:
                file = open(self.filePath, "r")
                self.message = file.read()
            except Exception as r:
                print('error: %s' % r)
                return
        else:
            print("error")
        # file = open(self.filePath, "r")
        # self.message = file.read()
        k = len(self.message)
        self.split = random.randint(1, k)
        if isinstance(self.mpc, Mpc):
            print("client is ready for MPC ")
            self.mpc.set_message_client(self.iv, self.message[:self.split], self.message[self.split:], self.key)
        else:
            print("error! ")

    def encrypt_prefix(self):
        return Utils.aes_cbc_encrypt(self.iv, self.message[:self.split], self.key)

    def get_suffix(self):
        return self.message[self.split:]

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
    #     # ????????????
    #     return Utils.aes_cbc_encrypt(self.iv, message, self.key)
    #
    #     # ??????AES-CBC??????
    #     # this function return ciphertext in bytes
    #     # encrypt_message = Utils.aes_cbc_encrypt_split(self.iv, message, self.key)
    #     # return encrypt_message
    #
    # def decrypt_message(self, message):
    #     # ????????????
    #     # return Utils.aes_cbc_decrypt(self.iv, message, self.key)
    #
    #     # ??????AES-CBC??????
    #     # this function return plaintext in bytes
    #     decrypt_message = Utils.aes_cbc_decrypt_split(self.iv, message, self.key)
    #     return decrypt_message
