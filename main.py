from client import Client
from proxy import Proxy
prover = Client()
verifier = Proxy()

# todo: 2P-HMAC
Tag = ""



# 2P-CBC
cipher_prefix = prover.encrpyt_prefix()
injected = verifier.inject(cipher_prefix, prover.key)
cipher_suffix = prover.encrpyt_suffix(injected)
cipher = verifier.sent_message(cipher_suffix+Tag)

challenge = prover.get_challenge(cipher)

verified = verifier.validate(challenge)
print("verification result: ", verified)
