from utils import Utils
class Proxy:
    def __init__(self):
        self.message = ''
        self.cipher = b''
        self.challenge = "*******THIS IS CHALLENGE********"
        self.prefixIndex = -1

    def inject(self, prefix, key):
        """
        :inputs: previous bytes
        :return: encrypted last byte
        following properties are meets:
        (1) Injection secrecy: The client cannot learn M∗ during the protocol interaction.2
        (2) Transcript privacy: The proxy does not learn anything about messages other than M∗.
        (3) Transcript integrity: The proxy should not be able to modify parts of the message transcript besides M∗.
        (4) Server obliviousness: Condition (2) in Definition 2 guarantees that the server cannot distinguish an SCI
             execution from a standard execution of the underlying SC protocol with the client.
        """
        c_last = prefix[-16:]
        c_injected = Utils.aes_cbc_encrypt(c_last, self.challenge, key)
        self.cipher = prefix + c_injected
        self.prefixIndex = len(prefix)
        return c_injected[-16:]

    def sent_message(self, suffix):
        return self.cipher + suffix

    def validate(self, challenge):
        return challenge == self.challenge
