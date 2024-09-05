from fastapi import FastAPI
from routers import tracks, studio, artists, albums

# from routers import artists, albums, tracks, studio

app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {"message": "Music recordings app"}

app.include_router(artists.router)
app.include_router(albums.router)
app.include_router(tracks.router)
app.include_router(studio.router)
