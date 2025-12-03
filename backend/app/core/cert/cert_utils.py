from cryptography import x509
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timezone

def load_cert(pem: bytes):
    return x509.load_pem_x509_certificate(pem, default_backend())

def is_cert_valid(cert) -> bool:
    # naive datetime → aware 로 변환
    not_before = cert.not_valid_before.replace(tzinfo=timezone.utc)
    not_after  = cert.not_valid_after.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)

    if not (not_before <= now <= not_after):
        return False

    # self-signed 인증서 거부 (원하면 다시 켜기)
    # if cert.issuer == cert.subject:
    #     return False

    return True