from Cryptodome.Cipher import AES
from Cryptodome import Random
from utils import Utils


class Mpc:
    # 16 bytes AES-CBC
    def __init__(self):
        self.KeyReady = False
        self.MessageReady = False
        self.start = False
        self.IV = ''
        self.Key = ''
        self.Prefix = ''
        self.Suffix = ''
        self.Message = ''
        self.Output = ''

    def set_message_client(self, iv, prefix, suffix, key):
        self.IV = iv
        self.Prefix = prefix
        self.Suffix = suffix
        self.Key = key
        self.KeyReady = True
        if self.check():
            Utils.send_message_using_SMTP(self.aes_2p_cbc_de(self.Output))

    def set_message_proxy(self, MessageValue):
        self.Message = MessageValue
        self.MessageReady = True
        if self.check():
            Utils.send_message_using_SMTP(self.aes_2p_cbc_de(self.Output))

    def check(self):
        if self.KeyReady == True and self.MessageReady == True and self.start == False:
            self.start = True
            self.Output = self.aes_2p_cbc_en()
            self.start = False
            return True
        elif not self.KeyReady:
            print("Then we need client's Key ")
            return False
        elif not self.MessageReady:
            print("Then we need proxy's Message ")
            return False
        else:
            print("not Ready ")
            return False

    def aes_2p_cbc_en(self):
        if self.start:
            return Utils.aes_cbc_encrypt(self.IV, self.Prefix + self.Message + self.Suffix, self.Key)
        else:
            print("not start!")
            return 0

    def aes_2p_cbc_de(self, message):
        if self.KeyReady:
            return Utils.aes_cbc_decrypt(self.IV, message, self.Key)
