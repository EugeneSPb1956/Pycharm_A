from ..backend.db_al import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
# from app1.models.artists import Artists

class Albums(Base):
    __tablename__ = 'albums'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    artist_id = Column(Integer, ForeignKey('artists.id'))
    studio_id = Column(Integer, ForeignKey('studio.id'))
    lable = Column(String)
    city = Column(String)
    release = Column(Integer)
    genre = Column(String)
    price = Column(Float)
    parent_id = Column(Integer, ForeignKey('albums.id'), nullable=True)

    artists = relationship('Artists', back_populates='albums')
    # category = relationship('Category', back_populates='products')
    studio = relationship('Studio', back_populates='albums')

    tracks = relationship("Tracks", back_populates="albums")
    # products = relationship("Product", back_populates="category")



class Studio(Base):
    __tablename__ = 'studio'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)
    city = Column(String)

    albums = relationship('Albums', back_populates='studio')
    # products = relationship("Product", back_populates="category")


from sqlalchemy.schema import CreateTable
print(CreateTable(Albums.__table__))
print(CreateTable(Studio.__table__))
