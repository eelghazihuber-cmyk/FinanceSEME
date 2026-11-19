from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.deps import get_current_user, own_account
from app.models import Account
from app.schemas import CurrentUser

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/", response_model=list[schemas.AccountRead])
def list_accounts(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    return db.scalars(select(Account).where(Account.user_id == user.id).order_by(Account.id)).all()


@router.post("/", response_model=schemas.AccountRead, status_code=201)
def create_account(
    data: schemas.AccountCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    account = Account(user_id=user.id, **data.model_dump())
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@router.put("/{account_id}", response_model=schemas.AccountRead)
def update_account(
    account_id: int,
    data: schemas.AccountCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    account = own_account(db, user, account_id)
    for key, value in data.model_dump().items():
        setattr(account, key, value)
    db.commit()
    db.refresh(account)
    return account


@router.delete("/{account_id}", status_code=204)
def delete_account(
    account_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    # TODO: Buchungen, Belege und Fixkosten des Kontos mitlöschen (Phase 2)
    db.delete(own_account(db, user, account_id))
    db.commit()
