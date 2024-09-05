
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..backend.db_depends import get_db
from typing import Annotated

from ..models.albums import Albums
from sqlalchemy import insert
from ..schemas import CreateAlbums

# from slugify import slugify
from sqlalchemy import select
from sqlalchemy import update

router = APIRouter(prefix='/albums', tags=['albums'])


@router.get('/')
async def all_albums(db: Annotated[Session, Depends(get_db)]):
    # albums = db.scalars(select(Albums).where(Albums.is_active == True, Albums.stock > 0)).all()
    albums = db.scalars(select(Albums).all())
    if albums is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no albums'
        )
    return albums

@router.post('/create')
async def create_albums(db: Annotated[Session, Depends(get_db)], create_albums: CreateAlbums):
    db.execute(insert(Albums).values(title=create_albums.title,
                                     artist_id=create_albums.artist_id,
                                     studio_id=create_albums.studio.id,
                                     lable=create_albums.lable,
                                     city=create_albums.city,
                                     release=create_albums.release,
                                     genre=create_albums.genre,
                                     price=create_albums.price))
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


@router.get('/detail/{artists_id}')
async def albums_detail(db: Annotated[Session, Depends(get_db)], artists_id: int):
    albums = db.scalar(select(Albums).where(Albums.artist_id == artists_id))
    if not albums:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no albums'
        )
    return albums


@router.put('/detail/{albums_id}')
async def update_albums(db: Annotated[Session, Depends(get_db)], albums_id: int,
                         update_albums_model: CreateAlbums):
    albums_update = db.scalar(select(Albums).where(Albums.id == albums_id))
    if albums_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no albums found'
        )

    db.execute(update(Albums).where(Albums.id == albums_id)
               .values(title=update_albums_model.title,
                       artist_id=update_albums_model.artist_id,
                       studio_id=update_albums_model.studio_id,
                       lable=update_albums_model.lable,
                       city=update_albums_model.city,
                       release=update_albums_model.release,
                       genre=update_albums_model.genre,
                       price=update_albums_model.price))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Albums update is successful'
    }

@router.delete('/delete')  # delete a row from table
async def delete_albums(db: Annotated[Session, Depends(get_db)], albums_id: int):
    albums_delete = db.scalar(select(Albums).where(Albums.id == albums_id))
    if albums_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no album found'
        )
    # db.execute(update(Albums).where(Albums.id == albums_id).values(is_active=False))  #  ???
    db.delete().where(Albums.id == albums_id)
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Album delete is successful'
    }
