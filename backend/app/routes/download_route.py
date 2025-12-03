from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from app.services.storage_service import get_file_meta, list_files_by_owner

import os
import zipfile
from io import BytesIO

# 라우터 설정
router = APIRouter(prefix="/download", tags=["download"])


# ============================================
# 1) 암호화된 파일 다운로드
# ============================================
@router.get("/{file_id}")
async def download_file(file_id: str):
    doc = get_file_meta(file_id)
    if not doc:
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")

    return FileResponse(
        path=doc["enc_path"],
        media_type="application/octet-stream",
        filename=f"{doc.get('original_filename', 'encrypted')}.enc",
    )


# ============================================
# 2) 사용자 파일 목록 조회
# ============================================
@router.get("/list/{owner_id}")
async def list_files(owner_id: str):
    docs = list_files_by_owner(owner_id)

    files = []
    for d in docs:
        files.append(
            {
                "file_id": str(d.get("_id")),
                "title": d.get("title"),
                "original_filename": d.get("original_filename"),
                "created_at": d.get("created_at"),
            }
        )

    return {"files": files}


# ============================================
# 3) RSA로 암호화된 AES 키 다운로드
# ============================================
@router.get("/key/{file_id}")
async def download_key(file_id: str):
    doc = get_file_meta(file_id)
    if not doc:
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")

    return FileResponse(
        path=doc["key_path"],
        media_type="application/octet-stream",
        filename=f"{file_id}.keyenc",
    )


# ============================================
# 4) ZIP 번들 다운로드 (file + key + hash + README)
# ============================================

# README 템플릿 위치
README_PATH = os.path.join(
    os.path.dirname(__file__), "../resources/README_TEMPLATE.txt"
)

@router.get("/bundle/{file_id}")
async def download_bundle(file_id: str):
    doc = get_file_meta(file_id)
    if not doc:
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")

    # README 텍스트 로드
    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme_text = f.read()
    except Exception:
        readme_text = "CrypServer README 파일을 불러올 수 없습니다.\n"

    # ZIP 생성
    memory = BytesIO()
    try:
        with zipfile.ZipFile(memory, "w", zipfile.ZIP_DEFLATED) as z:
            z.write(doc["enc_path"], arcname="file.enc")
            z.write(doc["key_path"], arcname="aes_key.keyenc")
            z.write(doc["hash_path"], arcname="file.sha256")
            z.writestr("README.txt", readme_text)
    except Exception as e:
        raise HTTPException(500, f"ZIP 생성 중 오류 발생: {e}")

    memory.seek(0)

    # 🔥 ZIP 파일 이름을 '원본 파일명.zip' 으로 설정
    original_name = doc.get("original_filename", file_id)
    base_name = os.path.splitext(original_name)[0]   # 확장자 제거

    return StreamingResponse(
        memory,
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename={base_name}.zip"
        }
    )
