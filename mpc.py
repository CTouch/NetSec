from Cryptodome.Cipher import AES
from Cryptodome import Random

# following Protocol 4: 2P-CBC
class Mpc:
    # 16 bytes AES-CBC
    def __init__(self):
        self.KeyReady = False
        self.MessageReady = False
        self.Key = ''
        self.Message = ''

    def set_key(self, KeyValue):
        pass

    def set_message(self, MessageValue):
        pass

    def aes_2p_cbc(self):

