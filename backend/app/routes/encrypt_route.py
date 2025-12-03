from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.encrypt_service import encrypt_file

# cryptography 관련 (PKI 활성 모드에서만 사용)
from cryptography import x509
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

router = APIRouter()

TEST_MODE = True
# TEST_MODE = False

@router.post("/")
async def upload_and_encrypt(
    file: UploadFile = File(...),
    cert: UploadFile = File(...),
    owner_id: str = Form(...)
):
    file_bytes = await file.read()
    cert_bytes = await cert.read()

    # ------------------------------------------------------------
    # 🔵 TEST MODE
    # ------------------------------------------------------------
    if TEST_MODE:
        # try:
        #     file_id = encrypt_file(file_bytes, cert_bytes, file.filename, owner_id)
        # except Exception as e:
        #     raise HTTPException(status_code=500, detail=f"암호화 실패: {str(e)}")
        # 디버그용, try/except 비활성화
        file_id = encrypt_file(file_bytes, cert_bytes, file.filename, owner_id)


        return {
            "file_id": file_id,
            "mode": "TEST_MODE (PKI 검증 비활성화)",
            "message": "업로드 및 암호화 성공"
        }

    # ------------------------------------------------------------
    # 🔒 FULL PKI MODE
    # ------------------------------------------------------------
    try:
        parsed_cert = x509.load_pem_x509_certificate(cert_bytes)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="올바른 인증서 형식이 아닙니다. X.509 PEM 인증서를 업로드하세요."
        )

    try:
        with open("ca_public.pem", "rb") as f:
            ca_pub = serialization.load_pem_public_key(f.read())

        ca_pub.verify(
            parsed_cert.signature,
            parsed_cert.tbs_certificate_bytes,
            padding.PKCS1v15(),
            parsed_cert.signature_hash_algorithm,
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="CA에서 발급한 인증서가 아닙니다. CA 검증을 통과하세요."
        )

    # 🔥 여기서도 owner_id 반드시 넣어야 함
    try:
        file_id = encrypt_file(file_bytes, cert_bytes, file.filename, owner_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"암호화 실패: {str(e)}")

    return {
        "file_id": file_id,
        "mode": "FULL_PKI_MODE",
        "message": "업로드 및 암호화 성공 (PKI 검증 통과)"
    }
