from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import encrypt_route, download_route

app = FastAPI(title="Hybrid Encryption Server")

# CORS (개발 편의를 위해 전체 허용 – 배포 시 도메인 제한 권장)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우트 등록
app.include_router(encrypt_route.router, prefix="/encrypt", tags=["encrypt"])
app.include_router(download_route.router)  # 이미 /download prefix 있음


@app.get("/")
def root():
    return {"message": "Hybrid Encryption Server Running"}
