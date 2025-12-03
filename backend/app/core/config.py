import os

# 암호화 파일들을 저장할 폴더
STORAGE_DIR = "./storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

#MongoDB 주소
MONGO_URI = "mongodb+srv://jannerf43:sWX66CLXMAiplzM6@cluster0.p2wubz1.mongodb.net/"

# DB 이름
DB_NAME = "crypto_serverr"

# CA 인증서 파일 경로
CA_CERT_PATH = None