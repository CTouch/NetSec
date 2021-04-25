from utils import Utils
import random
from mpc import Mpc


class Proxy:
    def __init__(self, mpc):
        self.message = ''
        self.filePath = 'ProxyText.txt'
        self.mpc = mpc
        self.cipher_prefix = ''

    def set_cipher_prefix(self, prefix):
        self.cipher_prefix = prefix

    def start(self):
        print("How do you set your injection Message : 1->terminal input 2->file ")
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
        # message = file.read()
        if isinstance(self.mpc, Mpc):
            print("Proxy is ready for MPC ")
            self.mpc.set_message_proxy(self.message)
        else:
            print("error! ")
    #
    # def set(self, filePath):
    #     self.filePath = filePath
