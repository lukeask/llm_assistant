from fastapi import APIRouter, File, UploadFile
import shutil
import time
import redis
import requests

from setup import WEB_SERVER_URL, REDIS_HOST, REDIS_PORT, LIVE_AUDIO_QUEUE, REDIS_PASSWORD, REDIS_USERNAME

router = APIRouter()
@router.post("/liveaudio")
async def upload_webm_file(file: UploadFile = File(...)):
    filename = str(time.time())
    file_location = f"./uploaded_files/liveaudio/{filename}.webm"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    r = redis(host = REDIS_HOST,
            password=REDIS_PASSWORD,
            port = REDIS_PORT,
            username=REDIS_USERNAME,
            password=REDIS_PASSWORD)
    
    r.rpush(LIVE_AUDIO_QUEUE, file_location)
    return {"message": "Webm file uploaded successfully"}

@router.post("/play_audio")
async def upload_wav(file: UploadFile = File(...)):
    filename = str(time.time())
    file_location = f"./public/wavs/{filename}.wav"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    wav_url = f"http://{WEB_SERVER_URL}/public/wavs/{filename}.wav"
    await requests.post(f"{WEB_SERVER_URL}/ws/play_wav_url", data=wav_url)
    return {"message": "Audio file uploaded and played successfully"}
    