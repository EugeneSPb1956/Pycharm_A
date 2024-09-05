
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..backend.db_depends import get_db
from typing import Annotated

from ..models.albums import Studio
from sqlalchemy import insert
from ..schemas import CreateStudio

# from slugify import slugify
from sqlalchemy import select

router = APIRouter(prefix='/studio', tags=['studio'])


@router.get('/')
async def all_products(db: Annotated[Session, Depends(get_db)]):
    # products = db.scalars(select(Product).where(Product.is_active == True, Product.stock > 0)).all()
    studio = db.scalars(select(Studio).all())
    if studio is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no studio records'
        )
    return studio

@router.post('/create')
async def create_studio(db: Annotated[Session, Depends(get_db)], create_studio: CreateStudio):
    db.execute(insert(Studio).values(name=create_studio.name,
                                     country=create_studio.country,
                                     city=create_studio.city))
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


# @router.get('/detail/{product_slug}')
# async def product_detail(db: Annotated[Session, Depends(get_db)], product_slug: str):
#     product = db.scalar(
#         select(Product).where(Product.slug == product_slug, Product.is_active == True, Product.stock > 0))
#     if not product:
#         return HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='There are no product'
#         )
#     return product
#

# @router.put('/detail/{product_slug}')
# async def update_product(db: Annotated[Session, Depends(get_db)], product_slug: str,
#                          update_product_model: CreateProduct):
#     product_update = db.scalar(select(Product).where(Product.slug == product_slug))
#     if product_update is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='There is no product found'
#         )
#
#     db.execute(update(Product).where(Product.slug == product_slug)
#                .values(name=update_product_model.name,
#                        description=update_product_model.description,
#                        price=update_product_model.price,
#                        image_url=update_product_model.image_url,
#                        stock=update_product_model.stock,
#                        category_id=update_product_model.category,
#                        slug=slugify(update_product_model.name)))
#     db.commit()
#     return {
#         'status_code': status.HTTP_200_OK,
#         'transaction': 'Product update is successful'
#     }

@router.delete('/delete')  # delete a row from table
async def delete_studio(db: Annotated[Session, Depends(get_db)], studio_id: int):
    studio_delete = db.scalar(select(Studio).where(Studio.id == studio_id))
    if studio_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No studio is found'
        )
    # db.execute(update(Albums).where(Albums.id == albums_id).values(is_active=False))  #  ???
    db.delete().where(Studio.id == studio_id)
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Studio delete is successful'
    }
