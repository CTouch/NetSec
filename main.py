from client import Client
from mpc import Mpc
from proxy import Proxy


mpc = Mpc()

print("MPC is ready for computation, please initialize client and proxy:(Press any key to continue)")
input()
print("then we set our client:")
client = Client(mpc)
client.start()

# print(mpc.Prefix, mpc.Suffix, mpc.Key, mpc.IV)
print("Press any key to continue:")
input()
print("then we set our proxy:")
proxy = Proxy(mpc)
proxy.start()


# print("Next we check for the injection information:")
# print("Please enter the content of the email:")
# ciphertext = client.encrpyt_message()
# print(str(client.decrypt_message(ciphertext), 'utf-8'))
# a = [1, 2, 3, 4]
# a.reverse()
# b = a[1:]
# b.extend([0])
# print(b)
