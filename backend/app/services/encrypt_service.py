# ======================================================
# TEST_MODE 설정
# ======================================================
TEST_MODE = True
# TEST_MODE = False  # ← PKI 정식 모드로 전환 시 변경

from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives import serialization

from app.core.cert.cert_utils import load_cert, is_cert_valid
from app.core.crypto.aes import aes_gcm_encrypt
from app.core.crypto.rsa_crypto import rsa_wrap_key
from app.core.crypto.hash_algo import sha256_hex
from app.services.storage_service import save_encrypted_files


def encrypt_file_with_cert(file_data: bytes, cert_pem: bytes, filename: str,
    owner_id: str,  ) -> str:

    # ======================================================
    # 🔥 TEST MODE (현재 사용)
    #  - 인증서 형식 검사 없음
    #  - 인증서 유효성 검사 없음
    #  - cert_pem 파싱 실패 시 test용 공개키 생성하여 사용
    # ======================================================
    if TEST_MODE:
        try:
            cert = load_cert(cert_pem)
            pub_key = cert.public_key()
        except:
            # 테스트 공개키 생성 (가짜 공개키 생성)
            from cryptography.hazmat.primitives.asymmetric import rsa
            pub_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            ).public_key()

        pub_pem = pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    # ======================================================
    # 🔐 PKI MODE (정식)
    # ======================================================
    else:
        cert = load_cert(cert_pem)

        if not is_cert_valid(cert):
            raise ValueError("유효하지 않은 인증서입니다.")

        pub_key = cert.public_key()

        pub_pem = pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    # AES 암호화 동일
    aes_key = get_random_bytes(32)
    enc_blob = aes_gcm_encrypt(aes_key, file_data)
    enc_key = rsa_wrap_key(pub_pem, aes_key)
    file_hash = sha256_hex(file_data)

    file_id = save_encrypted_files(enc_blob, enc_key, file_hash, filename, owner_id)

    return file_id


# encrypt_route가 호출하는 함수(wrapper)
def encrypt_file(file_data: bytes, cert_pem: bytes, filename: str,owner_id: str, ) -> str:
    return encrypt_file_with_cert(file_data, cert_pem, filename, owner_id)
