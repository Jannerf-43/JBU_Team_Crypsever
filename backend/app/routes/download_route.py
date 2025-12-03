from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.db.mongo import files_collection

router = APIRouter(prefix="/download", tags=["download"])

@router.get("/{file_id}")
async def download_file(file_id: str):
    doc = files_collection.find_one({"_id": file_id})
    if not doc:
        raise HTTPException(404, "파일을 찾을 수 없습니다.")

    return FileResponse(
        doc["enc_path"],
        media_type="application/octet-stream",
        filename=f"{doc['original_filename']}.enc"
    )

@router.get("/list/{owner_id}")
async def list_files(owner_id: str):
    docs = list(files_collection.find({"owner_id": owner_id}))
    # ObjectId가 아니라 _id가 string이라도, 안전하게 문자열로 캐스팅
    for d in docs:
        d["_id"] = str(d["_id"])
    return {"files": docs}