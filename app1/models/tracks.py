from ..backend.db_al import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
# from app1.models.albums import Albums


class Tracks(Base):
    __tablename__ = 'tracks'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    album_id = Column(Integer, ForeignKey('albums.id'))
    number = Column(Integer, unique=True, index=True)
    title = Column(String)
    writer = Column(String)
    lyrics = Column(String)
    length = Column(Float)
    parent_id = Column(Integer, ForeignKey('tracks.id'), nullable=True)

    albums = relationship('Albums', back_populates='tracks')
    # category = relationship('Category', back_populates='products')

from sqlalchemy.schema import CreateTable
print(CreateTable(Tracks.__table__))
