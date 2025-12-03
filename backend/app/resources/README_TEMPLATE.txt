CrypServer 암호화 ZIP 안내

file.enc          : AES-256 암호화된 파일
aes_key.keyenc    : RSA 공개키로 암호화된 AES 대칭키
file.sha256       : 무결성 확인용 SHA-256 해시값

[복호화 절차]
1. RSA 개인키로 aes_key.keyenc 복호화 → AES 키 획득
2. 해당 AES 키로 file.enc 복호화 → 원본 파일 생성
