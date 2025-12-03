from Crypto.Hash import SHA256

def sha256_hex(data: bytes) -> str:
  return SHA256.new(data).hexdigest()