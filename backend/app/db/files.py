from app.db.mongo import db
from datetime import datetime

collection = db["files"]

def insert_file_meta(meta: dict):
    meta["created_at"] = datetime.utcnow()
    collection.insert_one(meta)

def get_files_by_owner(owner_id: str):
    results = list(collection.find(
        {"owner_id": owner_id},
        {"_id": 0}
    ))
    return results

def get_file_meta(file_id: str):
    return collection.find_one({"file_id": file_id}, {"_id": 0})
