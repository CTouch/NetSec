from Cryptodome.Cipher import AES
from Cryptodome import Random
import re
import smtplib
from email.mime.text import MIMEText


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
        tmp = data + '!' * (16 - len(data) % 16)
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

    @staticmethod
    def send_message_using_SMTP(message, sender="953918409@qq.com",
                                password="vpheqiododknbehb",
                                receiver="941874266@qq.com",
                                server="smtp.qq.com"):
        msg = MIMEText("这是我用python发送的邮件", "plain", "utf-8") if len(message) == 0 else MIMEText(message, "plain",
                                                                                               "utf-8")
        try:
            # 不能直接使用smtplib.SMTP来实例化，第三方邮箱会认为它是不安全的而报错
            # 使用加密过的SMTP_SSL来实例化，它负责让服务器做出具体操作，它有两个参数
            # 第一个是服务器地址，但它是bytes格式，所以需要编码
            # 第二个参数是服务器的接受访问端口，SMTP_SSL协议默认端口是465
            srv = smtplib.SMTP_SSL(server.encode(), 465)
            # 使用授权码登录你的QQ邮箱
            srv.login(sender, password)
            # 使用sendmail方法来发送邮件，它有三个参数
            # 第一个是发送地址
            # 第二个是接受地址，是list格式，意在同时发送给多个邮箱
            # 第三个是发送内容，作为字符串发送
            srv.sendmail(sender, [receiver], msg.as_string())
            print('发送成功')
        except Exception:
            print('发送失败')
        finally:
            # 无论发送成功还是失败都要退出你的QQ邮箱
            srv.quit()

        # # MIMEText三个主要参数
        # # 1. 邮件内容
        # # 2. MIME子类型，在此案例我们用plain表示text类型
        # # 3. 邮件编码格式，一定要用"utf-8"编码，因为内容可能包含非英文字符，不用的可能收到的邮件是乱码
        # msg = MIMEText("这是我用python发送的邮件", "plain", "utf-8")
        # # vpheqiododknbehb
        #
        # # 发送email地址，填入你授权码的那个邮箱地址，此处地址是我常用QQ的地址
        # from_addr = "953918409@qq.com"
        # # 此处密码填你之前获得的授权码，不是你的QQ邮箱密码
        # from_pwd = "vpheqiododknbehb"#此处我是随便写的
        #
        # # 接受email地址，填入你要发送的邮箱地址，此处地址是我另外一个QQ小号的邮箱地址
        # to_addr = "941874266@qq.com"
        # # 输入SMTP服务器地址，并使用该服务器给你发送电子邮件
        # # 此处根据不同的邮件服务商有不同的值，
        # # 现在基本任何一家邮件服务商，如果采用第三方收发邮件，都需要开启授权选项
        # # 腾讯QQ邮箱的SMTP地址是"smtp.qq.com"
        # smtp_srv = "smtp.qq.com"
