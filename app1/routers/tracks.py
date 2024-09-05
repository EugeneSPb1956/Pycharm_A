
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..backend.db_depends import get_db
from typing import Annotated

from ..models.tracks import Tracks
from sqlalchemy import insert
from ..schemas import CreateTracks

# from slugify import slugify
from sqlalchemy import select
from sqlalchemy import update

router = APIRouter(prefix='/albums', tags=['albums'])


@router.get('/')
async def all_tracks(db: Annotated[Session, Depends(get_db)]):
    # albums = db.scalars(select(Albums).where(Albums.is_active == True, Albums.stock > 0)).all()
    tracks = db.scalars(select(Tracks).all())
    if tracks is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no tracks'
        )
    return tracks

@router.post('/create')
async def create_tracks(db: Annotated[Session, Depends(get_db)], create_tracks: CreateTracks):
    db.execute(insert(Tracks).values(album_id=create_tracks.album_id,
                                     number=create_tracks.number,
                                     title=create_tracks.title,
                                     writer=create_tracks.writer,
                                     lyrics=create_tracks.lyrics,
                                     length=create_tracks.length))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


# @router.get('/{category_slug}')
# async def product_by_category(db: Annotated[Session, Depends(get_db)], category_slug: str):
#     category = db.scalar(select(Category).where(Category.slug == category_slug))
#     if category is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='Category not found'
#         )
#     subcategories = db.scalars(select(Category).where(Category.parent_id == category.id)).all()
#     categories_and_subcategories = [category.id] + [i.id for i in subcategories]
#     products_category = db.scalars(
#         select(Product).where(Product.category_id.in_(categories_and_subcategories), Product.is_active == True,
#                               Product.stock > 0)).all()
#     return products_category


@router.get('/detail/{albums_id}')
async def tracks_detail(db: Annotated[Session, Depends(get_db)], albums_id: int):
    tracks = db.scalar(select(Tracks).where(Tracks.albums_id == albums_id))
    if not tracks:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no tracks'
        )
    return tracks


@router.put('/detail/{tracks_id}')
async def update_tracks(db: Annotated[Session, Depends(get_db)], tracks_id: int,
                         update_albums_model: CreateTracks):
    tracks_update = db.scalar(select(Tracks).where(Tracks.id == tracks_id))
    if tracks_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no tracks found'
        )

    db.execute(update(Tracks).where(Tracks.id == tracks_id)
               .values(album_id=create_tracks.album_id,
                       number=create_tracks.number,
                       title=create_tracks.title,
                       writer=create_tracks.writer,
                       lyrics=create_tracks.lyrics,
                       length=create_tracks.length))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Tracks update is successful'
    }

@router.delete('/delete')  # delete a row from table
async def delete_tracks(db: Annotated[Session, Depends(get_db)], tracks_id: int):
    tracks_delete = db.scalar(select(Tracks).where(Tracks.id == tracks_id))
    if tracks_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no tracks found'
        )
    # db.execute(update(Albums).where(Albums.id == albums_id).values(is_active=False))  #  ???
    db.delete().where(Tracks.id == tracks_id)
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Tracks delete is successful'
    }
