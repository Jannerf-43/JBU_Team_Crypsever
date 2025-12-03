import os
from uuid import uuid4
from datetime import datetime, timezone

from app.core.config import STORAGE_DIR
from app.db.mongo import files_collection


def save_encrypted_files(
    enc_blob: bytes,
    enc_key: bytes,
    file_hash: str,
    original_name: str,
    owner_id: str,
    title: str,
) -> str:
    """암호화된 파일/키/해시를 디스크에 저장하고
    해당 메타데이터를 MongoDB 에 기록한다.
    """

    file_id = str(uuid4())

    enc_path = os.path.join(STORAGE_DIR, f"{file_id}.enc")
    key_path = os.path.join(STORAGE_DIR, f"{file_id}.keyenc")
    hash_path = os.path.join(STORAGE_DIR, f"{file_id}.sha256")

    # 1) 파일 시스템에 저장
    with open(enc_path, "wb") as f:
        f.write(enc_blob)

    with open(key_path, "wb") as f:
        f.write(enc_key)

    with open(hash_path, "w", encoding="utf-8") as f:
        f.write(file_hash + "\n")

    # 2) 메타데이터 MongoDB 저장
    now = datetime.now(timezone.utc)

    files_collection.insert_one(
        {
            "_id": file_id,
            "owner_id": owner_id,
            "title": title,
            "original_filename": original_name,
            "enc_path": enc_path,
            "key_path": key_path,
            "hash_path": hash_path,
            "file_hash": file_hash,
            "created_at": now,
        }
    )

    return file_id


def get_file_meta(file_id: str):
    return files_collection.find_one({"_id": file_id})


def list_files_by_owner(owner_id: str):
    return list(
        files_collection.find({"owner_id": owner_id}).sort("created_at", -1)
    )
