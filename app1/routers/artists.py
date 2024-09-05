from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..backend.db_depends import get_db
# from backend.db_depends import get_db
from typing import Annotated

from ..models.artists import Artists
# from app1.models import *
from sqlalchemy import insert
# from app.schemas import CreateCategory
from ..schemas import CreateArtists

# from slugify import slugify

# router = APIRouter(prefix='/category', tags=['category'])
router = APIRouter(prefix='/artists', tags=['artists'])

@router.post('/create')
# async def create_artists(db: Annotated[Session, Depends(get_db)], create_artists: CreateArtists):
# db.execute(insert(Category).values(name=create_category.name,
#                                    parent_id=create_category.parent_id,
#                                    slug=slugify(create_category.name)))
async def create_artists(db: Annotated[Session, Depends(get_db)], create_artists: CreateArtists):
    db.execute(insert(Artists).values(name=create_artists.name,
                                      country=create_artists.country,
                                      city=create_artists.city,
                                      year1=create_artists.year1,
                                      year2=create_artists.year2,
                                      active=create_artists.active,
                                      parent_id=create_artists.parent_id))

    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }
# ---------------------------------
from sqlalchemy import select


# @router.get('/all_categories')
# async def get_all_categories(db: Annotated[Session, Depends(get_db)]):
#     categories = db.scalars(select(Category).where(Category.is_active == True)).all()
#     return categories
@router.get('/all_artists')
async def get_all_artists(db: Annotated[Session, Depends(get_db)]):
    artists = db.scalars(select(Artists).where(Artists.name == 'Queen')).all()
    return artists

# -----------------------------
# @router.put('/update_category')
# async def update_category(db: Annotated[Session, Depends(get_db)], category_id: int, update_category: CreateCategory):
#     category = db.scalar(select(Category).where(Category.id == category_id))
#     if category is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='There is no category found'
#         )
@router.put('/update_artists')
async def update_artists(db: Annotated[Session, Depends(get_db)], artists_id: int,
                          update_artists: CreateArtists):
    artists = db.scalar(select(Artists).where(Artists.id == artists_id))
    if artists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no artist found'
        )

    # db.execute(update(Category).where(Category.id == category_id).values(
    #         name=update_category.name,
    #         slug=slugify(update_category.name),
    #         parent_id=update_category.parent_id))
    db.execute(update(Artists).where(Artists.id == artists_id).values(
            country=update_artists.country,
            city=update_artists.city,
            year1=update_artists.year1,
            year2=update_artists.year2,
            active=update_artists.active,
            parent_id=update_artists.parent_id))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Category update is successful'
    }

# -----------------------------------------------
from sqlalchemy import update


@router.delete('/delete')
# async def delete_category(db: Annotated[Session, Depends(get_db)], category_id: int):
#     category = db.scalar(select(Category).where(Category.id == category_id))
#     if category is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='There is no category found'
#         )
#     db.execute(update(Category).where(Category.id == category_id).values(is_active=False))
async def delete_artists(db: Annotated[Session, Depends(get_db)], artists_id: int):
    artists = db.scalar(select(Artists).where(Artists.id == artists_id))
    if artists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no category found'
        )
    db.execute(update(Artists).where(Artists.id == artists_id).values(active=False))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Category delete is successful'
    }