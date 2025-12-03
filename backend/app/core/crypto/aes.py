from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def aes_gcm_encrypt(key: bytes, plaintxt: bytes) -> bytes:
  cipher = AES.new(key, AES.MODE_GCM)
  ciphertext, tag = cipher.encrypt_and_digest(plaintxt)
  return cipher.nonce + tag + ciphertext

def aes_gcm_decrypt(key: bytes, enc_blob:bytes) -> bytes:
  nonce = enc_blob[:16]
  tag = enc_blob[16:32]
  ciphertext = enc_blob[32:]
  cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
  return cipher.decrypt_and_verify(ciphertext, tag)