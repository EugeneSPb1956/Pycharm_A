from ..backend.db_al import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

class Artists(Base):
    __tablename__ = 'artists'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)
    city = Column(String)
    year1 = Column(Integer)
    year2 = Column(Integer)
    active = Column(Boolean, default=True)
    parent_id = Column(Integer, ForeignKey('artists.id'), nullable=True)

    albums = relationship('Albums', back_populates='artists')
    # products = relationship("Product", back_populates="category")

from sqlalchemy.schema import CreateTable
print(CreateTable(Artists.__table__))