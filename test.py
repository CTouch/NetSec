from Cryptodome.Cipher import AES
from Cryptodome import Random


data = '需要加密的数据'

# 密钥key需要为16, 24, 32长度的字节类型数据.
# 我们使用AES-128位(16字节)来使用.
key = b'1234567890123456'   # 16bytes

# 还需要使用一个向量.
iv = Random.new().read(AES.block_size)  # 生成一个长度等于AES块大小并且不重复的密钥向量对象.

# 使用key和iv初始化AES对象, 使用MODE_CFB模式.
aesobj = AES.new(key, AES.MODE_CFB, iv)

# 加密的数据的长度需为16的倍数, 不足16则会自动补足.
# 将密钥向量加到加密后的密文开头, 一起传输(方便后面解密).
aescrypto = iv + aesobj.encrypt(data.encode())
print(aescrypto)

# 解密需要使用Key和iv生成新的AES对象.
aesobj2 = AES.new(key, AES.MODE_CFB, aescrypto[0:16])

# 使用新的AES对象来解密.
aescrypto2 = aesobj2.decrypt(aescrypto[16:])
print(aescrypto2.decode())  # 这里记得decode()哦
