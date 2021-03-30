from Cryptodome.Cipher import AES
from Cryptodome import Random
import re


class Utils:
    @staticmethod
    def add_16(data, padding_char='!'):
        if isinstance(padding_char, str):
            return data + padding_char[0] * (16 - (len(data)) % 16)
        else:
            return data + '!' * (16 - (len(data)) % 16)

    @staticmethod
    def split_with_16_length(message):
        return re.findall(r'.{16}', message)

    @staticmethod
    def aes_cbc_encrypt(message, key):
        # iv is the first sixteen chars in message, so as the encrypt_message
        iv = encrypt_message = message[0:16]
        iv = bytes(iv.encode())
        message_list = Utils.split_with_16_length(Utils.add_16(message[16:]))
        for M in message_list:
            aes = AES.new(key, AES.MODE_CBC, iv)
            cipher_text = aes.encrypt(M.encode())
            iv = bytes.fromhex(str(int(iv.hex(), 16) ^ int(cipher_text.hex(), 16), 16))
            encrypt_message += cipher_text.decode()
        return encrypt_message

    @staticmethod
    def sha_256(message):
        pass
