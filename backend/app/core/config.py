import os

STORAGE_DIR = "./storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("환경변수 MONGO_URI가 설정되지 않았습니다.")

DB_NAME = "crypto_server"   

CA_CERT_PATH = os.getenv("CA_CERT_PATH", None)
