from Crypto.Cipher import AES
from Crypto import Random
import re
import crypt


# str -> bytes : encode()
# bytes -> str : decode()
# bytes can only xor one by one
class Utils:
    # AES—CBC要用到的函数
    # @staticmethod
    # def bytes_xor(a, b):
    #     if len(a) == len(b):
    #         return bytes(a ^ b for (a, b) in zip(a, b))
    #     else:
    #         raise ValueError(AttributeError)

    @staticmethod
    def add_16(data):
        # return bytes
        tmp = data + '!' * ((16 - len(data.encode()) % 16) % 16)
        return tmp.encode()

    @staticmethod
    def remove_padding(message):
        # return string
        padding_char = b'!'
        # 这个真的恶心到我了
        while message[-1] == padding_char[0]:
            message = message[:-1]
        return message

    @staticmethod
    def aes_cbc_encrypt(iv, message, key):
        aes = AES.new(key, AES.MODE_CBC, iv)
        message = Utils.add_16(message)
        return aes.encrypt(message)

    @staticmethod
    def aes_cbc_decrypt(iv, message, key):
        aes = AES.new(key, AES.MODE_CBC, iv)
        message = aes.decrypt(message)
        return Utils.remove_padding(message)

    # 上面的部分是AES-CBC的直接加密或者解密，下面的是拆解AES-CBC加密解密
    @staticmethod
    def add_16_bytes(data, padding_char=b'!'):
        # data is string so we made it to bytes.
        data = data.encode()
        # bytes array's padding
        if isinstance(padding_char, bytes) and len(padding_char) == 1:
            return data + padding_char * (16 - len(data) % 16)
        else:
            return data + b'!' * (16 - len(data) % 16)

    @staticmethod
    def split_with_16_length_bytes(message):
        # type(message) = <class:"bytes">
        # bytes array split
        # at first we use .{16} but \n is very important too !!!!!!!
        return re.findall(b'[\s\S]{16}', message)

    @staticmethod
    def aes_cbc_encrypt_split(iv, message, key, addition_function=None):
        # 拆解每一步的AES-CBC 可以方便进行进一步操作
        # message is a string, Key and iv are in bytes
        # output bytes

        encrypt_message = b''

        # because some char in string maybe decode to two bytes in bytes array
        # we need to change message to bytes array then give it a padding and split it
        message_list = Utils.split_with_16_length_bytes(Utils.add_16_bytes(message))
        # input parameter is in string type, but output is in bytes

        for M in message_list:
            aes = AES.new(key, AES.MODE_CBC, iv)
            cipher_text = aes.encrypt(M)
            # 这里其实可以加上自己的发挥 因为AES已经被拆开了 中间加入什么别的函数也可以提升一下强度
            # todo
            # addition_function()
            # 脑子抽了不知道什么要异或
            # iv = Utils.bytes_xor(iv, cipher_text)
            iv = cipher_text
            encrypt_message += cipher_text
        return encrypt_message

    @staticmethod
    def aes_cbc_decrypt_split(iv, message, key, addition_function=None):
        # 拆解每一步的AES-CBC 可以方便进行进一步操作
        # message iv key are all in bytes
        # output bytes

        decrypt_message = b''

        # because some char in string maybe decode to two bytes in bytes array
        # we need to change message to bytes array then give it a padding and split it
        message_list = Utils.split_with_16_length_bytes(message)
        # input parameter is in string type, but output is in bytes

        # reverse message_list and get iv_list
        message_list.reverse()
        iv_list = message_list[1:]
        iv_list.extend([iv])
        for M, iv in zip(message_list, iv_list):
            # 对应的在此位置进行逆操作 使得解密消息正确
            # addition_function()
            # todo
            aes = AES.new(key, AES.MODE_CBC, iv)
            cipher_text = aes.decrypt(M)
            decrypt_message = cipher_text + decrypt_message
        return Utils.remove_padding(decrypt_message)

    # 下面的部分就是其他要进行的加密解密函数
    @staticmethod
    def sha_256(message):
        pass
