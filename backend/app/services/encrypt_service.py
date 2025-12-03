from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives import serialization

from app.core.cert.cert_utils import load_cert, is_cert_valid
from app.core.crypto.aes import aes_gcm_encrypt
from app.core.crypto.rsa_crypto import rsa_wrap_key
from app.core.crypto.hash_algo import sha256_hex
from app.services.storage_service import save_encrypted_files

# -------------------------------------------------------
# TEST_MODE:
#   True  -> CA 검증 없이 cert 의 공개키만 사용 (self-signed 허용)
#   False -> is_cert_valid() 등을 통해 정식 검증 (추후 CA 서버 연동 시)
# -------------------------------------------------------
TEST_MODE = True
# TEST_MODE = False  # ← CA 서버 구축 후 이 값으로 바꾸면 됨


def encrypt_file_with_cert(
    file_data: bytes,
    cert_pem: bytes,
    filename: str,
    owner_id: str,
    title: str,
) -> str:
    """X.509 인증서를 이용해
    1) AES-256-GCM 으로 파일을 암호화하고
    2) AES 키를 인증서의 공개키(RSA)로 다시 암호화한 뒤
    3) 암호문/키/해시/메타데이터를 저장한다.
    """

    # 1) 인증서 파싱
    cert = load_cert(cert_pem)

    if not TEST_MODE:
        # 정식 모드에서는 유효기간, self-signed 여부, CA 체인 등 검증
        if not is_cert_valid(cert):
            raise ValueError("인증서가 유효하지 않습니다. (만료 또는 허용되지 않은 인증서)")

        # TODO: CA 서버, 체인 검증 로직 추가 (CA_CERT_PATH, OCSP 등)
    # TEST_MODE 인 경우: 단순히 형식만 맞으면 통과 (self-signed, 미검증 CA 모두 허용)

    # 2) 인증서에서 공개키 추출 → PEM 형태로 변환
    pub_key = cert.public_key()
    pub_pem = pub_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    # 3) AES 키 생성 및 파일 암호화
    aes_key = get_random_bytes(32)  # AES-256
    enc_blob = aes_gcm_encrypt(aes_key, file_data)  # nonce + tag + ciphertext
    file_hash = sha256_hex(file_data)

    # 4) AES 키를 공개키(RSA)로 감싸기 (wrap)
    enc_key = rsa_wrap_key(pub_pem, aes_key)

    # 5) 저장 (파일시스템 + MongoDB 메타데이터)
    file_id = save_encrypted_files(
        enc_blob=enc_blob,
        enc_key=enc_key,
        file_hash=file_hash,
        original_name=filename,
        owner_id=owner_id,
        title=title,
    )

    return file_id


def encrypt_file(file_data: bytes, cert_pem: bytes, filename: str, owner_id: str, title: str) -> str:
    """라우트에서 직접 호출하는 래퍼 함수"""
    return encrypt_file_with_cert(file_data, cert_pem, filename, owner_id, title)
