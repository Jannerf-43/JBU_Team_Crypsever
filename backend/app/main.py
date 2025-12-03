from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import encrypt_route, download_route
from app.routes.files_route import router as files_router

app = FastAPI(title="Hybrid Encryption Server")

# Files 라우트
app.include_router(files_router, prefix="/files", tags=["files"])

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Encryption 라우트
app.include_router(encrypt_route.router, prefix="/encrypt", tags=["encrypt"])

# Download 라우트 (중복 prefix 제거!!)
app.include_router(download_route.router)

@app.get("/")
def root():
    return {"message": "Hybrid Encryption Server Running"}
