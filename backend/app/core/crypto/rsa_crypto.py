from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def rsa_wrap_key(pub_pem: bytes, aes_key:bytes) -> bytes:
  pub = RSA.import_key(pub_pem)
  cipher = PKCS1_OAEP.new(pub)
  return cipher.encrypt(aes_key)

def rsa_unwrap_key(priv_pem: bytes, enc_key: bytes, passphrase=None) -> bytes:
  priv = RSA.import_key(priv_pem, passphrase=passphrase)
  cipher = PKCS1_OAEP.new(priv)
  return cipher.decrypt(enc_key)