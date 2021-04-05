from client import Client

client = Client()
ciphertext = client.encrpyt_message()
print(str(client.decrypt_message(ciphertext),'utf-8'))


# a = [1, 2, 3, 4]
# a.reverse()
# b = a[1:]
# b.extend([0])
# print(b)
