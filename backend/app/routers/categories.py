from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.deps import get_current_user, own_category
from app.models import Category
from app.schemas import CurrentUser

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[schemas.CategoryRead])
def list_categories(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    return db.scalars(select(Category).where(Category.user_id == user.id).order_by(Category.name)).all()


@router.post("/", response_model=schemas.CategoryRead, status_code=201)
def create_category(
    data: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    own_category(db, user, data.parent_id)
    category = Category(user_id=user.id, **data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put("/{category_id}", response_model=schemas.CategoryRead)
def update_category(
    category_id: int,
    data: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    category = own_category(db, user, category_id)
    own_category(db, user, data.parent_id)
    for key, value in data.model_dump().items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    # TODO: Buchungen dieser Kategorie auf "ohne Kategorie" setzen (Phase 2)
    db.delete(own_category(db, user, category_id))
    db.commit()
