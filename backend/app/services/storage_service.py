import os
from uuid import uuid4
from app.core.config import STORAGE_DIR
from app.db.mongo import files_collection

def save_encrypted_files(enc_blob: bytes,
    enc_key: bytes,
    file_hash: str,
    original_name: str,
    owner_id: str,   ):
    file_id = str(uuid4())

    enc_path = os.path.join(STORAGE_DIR, f"{file_id}.enc")
    key_path = os.path.join(STORAGE_DIR, f"{file_id}.keyenc")
    hash_path = os.path.join(STORAGE_DIR, f"{file_id}.sha256")

    with open(enc_path, "wb") as f:
        f.write(enc_blob)

    with open(key_path, "wb") as f:
        f.write(enc_key)

    with open(hash_path, "w", encoding="utf-8") as f:
        f.write(file_hash + "\n")

    files_collection.insert_one({
        "_id": file_id,
        "original_filename": original_name,
        "enc_path": enc_path,
        "key_path": key_path,
        "hash_path": hash_path,
        "owner_id": owner_id,        # 🔹 여기!
    })

    return file_id