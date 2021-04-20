from Cryptodome.Cipher import AES
from Cryptodome import Random
from utils import Utils


class Mpc:
    # 16 bytes AES-CBC
    def __init__(self):
        self.__KeyReady__ = False
        self.__MessageReady__ = False
        self.__start__ = False
        self.__IV__ = ''
        self.__Key__ = ''
        self.__Prefix__ = ''
        self.__Suffix__ = ''
        self.__Message__ = ''
        self.__Output__ = ''

    def set_message_client(self, iv, prefix, suffix, key):
        self.__IV__ = iv
        self.__Prefix__ = prefix
        self.__Suffix__ = suffix
        self.__Key__ = key
        self.__KeyReady__ = True
        if self.check():
            Utils.send_message_using_SMTP(self.aes_2p_cbc_de(self.__Output__))

    def set_message_proxy(self, MessageValue):
        self.__Message__ = MessageValue
        self.__MessageReady__ = True
        if self.check():
            Utils.send_message_using_SMTP(self.aes_2p_cbc_de(self.__Output__))

    def check(self):
        if self.__KeyReady__ == True and self.__MessageReady__ == True and self.__start__ == False:
            self.__start__ = True
            self.__Output__ = self.aes_2p_cbc_en()
            self.__start__ = False
            return True
        elif not self.__KeyReady__:
            print("Then we need client's Key ")
            return False
        elif not self.__MessageReady__:
            print("Then we need proxy's Message ")
            return False
        else:
            print("not Ready ")
            return False

    def aes_2p_cbc_en(self):
        if self.__start__:
            # return Utils.aes_cbc_encrypt(self.IV, self.Prefix + self.Message + self.Suffix, self.Key)
            return Utils.aes_cbc_encrypt_split(self.__IV__, self.__Prefix__ + self.__Message__ + self.__Suffix__,
                                               self.__Key__, Utils.little_xor)
        else:
            print("not start!")
            return 0

    def aes_2p_cbc_de(self, message):
        if self.__KeyReady__:
            # return Utils.aes_cbc_decrypt(self.IV, message, self.Key)
            return Utils.aes_cbc_decrypt_split(self.__IV__, message, self.__Key__, Utils.little_xor)
