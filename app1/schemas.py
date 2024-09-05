from pydantic import BaseModel


class CreateTracks(BaseModel):
    album_id: int
    number: int
    title: str
    writer: str
    lyrics: str
    length: float
    parent_id: int

class CreateStudio(BaseModel):
    name: str
    country: str
    city: str

class CreateAlbums(BaseModel):
    title: str
    artist_id: int
    studio_id: int
    lable: str
    city: str
    release: int
    genre: str
    price: float
    parent_id: int

class CreateArtists(BaseModel):
    name: str
    country: str
    city: str
    year1: int
    year2: int
    active: bool
    parent_id: int

