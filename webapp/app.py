from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import webpage, media_files

app = FastAPI()

app.include_router(webpage.router)
app.include_router(media_files.router)
app.mount("/public", StaticFiles(directory="./public"), name="public")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8011, reload=True)