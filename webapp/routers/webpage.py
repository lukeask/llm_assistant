from fastapi import APIRouter,Depends, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/")
async def webpage():
    return FileResponse("./public/index.html")