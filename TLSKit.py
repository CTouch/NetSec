from tlslite.api import *
# not ready yet
s = SMTP_TLS("----------.net", port=587)
s.ehlo()
s.starttls(x509Fingerprint="7e39be84a2e3a7ad071752e3001d931bf82c32dc")
