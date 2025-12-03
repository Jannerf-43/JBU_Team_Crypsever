from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.services.encrypt_service import encrypt_file

router = APIRouter()


@router.post("/")
async def upload_and_encrypt(
    file: UploadFile = File(...),
    cert: UploadFile = File(...),
    owner_id: str = Form(...),
    title: str = Form(...),
):
    """파일 + 인증서 업로드 후 암호화 수행

    - TEST_MODE 인 경우: self-signed / 미검증 cert 모두 허용
    - 정식 모드: encrypt_service 내부의 TEST_MODE = False 로 전환 후 사용
    """

    if not owner_id:
        raise HTTPException(status_code=400, detail="owner_id 가 필요합니다.")

    if not title:
        raise HTTPException(status_code=400, detail="제목(title)을 입력해야 합니다.")

    try:
        file_bytes = await file.read()
        cert_bytes = await cert.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"파일 읽기 실패: {str(e)}")

    if not file_bytes:
        raise HTTPException(status_code=400, detail="빈 파일입니다.")

    try:
        file_id = encrypt_file(file_bytes, cert_bytes, file.filename, owner_id, title)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"암호화 실패: {str(e)}")

    return {
        "file_id": file_id,
        "message": "업로드 및 암호화 성공",
        "title": title,
    }
