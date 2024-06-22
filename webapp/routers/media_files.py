from fastapi import APIRouter,Depends, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/wav/{file_name}")
async def post_media_file(file_name:str):
    return FileResponse("./public/wavs"+file_name, media_type="audio/wav")

@router.get("/pdf/{file_name}")
async def post_media_file(file_name:str):
    return FileResponse("./public/pdfs/"+file_name, media_type="application/pdf")