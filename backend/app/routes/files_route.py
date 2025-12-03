from fastapi import APIRouter, HTTPException, Query
from app.db.files import get_files_by_owner

router = APIRouter()

@router.get("/")
async def list_files(owner_id: str = Query(...)):
    files = get_files_by_owner(owner_id)
    
    return {"files": files}
