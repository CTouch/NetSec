from utils import Utils
from Crypto import Random
from Crypto.Cipher import AES


class Client:
    def __init__(self):
        self.key = b'0123456789ABCDEF'  # get a Key in bytes
        self.iv = Random.new().read(AES.block_size)  # get an iv in bytes
        self.filePath = "ClientMassage.txt"  # file needs to be sent
        self.prefixIndex = 32
        self.cipher_len = 0

    def encrpyt_prefix(self):
        file = open(self.filePath, "r")
        message = file.read()
        cipher_prefix = Utils.aes_cbc_encrypt(self.iv, message[:self.prefixIndex], self.key)
        self.cipher_len += len(cipher_prefix)
        return cipher_prefix

    def encrpyt_suffix(self, prev_cipher):
        file = open(self.filePath, "r")
        message = file.read()
        cipher_suffix = Utils.aes_cbc_encrypt(prev_cipher, message[self.prefixIndex:], self.key)
        self.cipher_len += len(cipher_suffix)
        return cipher_suffix

    def decrypt_message(self, message):
        return Utils.aes_cbc_decrypt(self.iv, message, self.key)

    def get_challenge(self, cipher):
        msg = self.decrypt_message(cipher).decode()
        len_challenge = len(cipher) - self.cipher_len
        challenge = msg[self.prefixIndex:self.prefixIndex + len_challenge]
        return challenge
