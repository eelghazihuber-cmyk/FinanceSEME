from datetime import date

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.deps import get_current_user, own_account, own_category
from app.models import Account, Transaction
from app.schemas import CurrentUser
from app.utils import todo

router = APIRouter(prefix="/transactions", tags=["transactions"])


def own_transaction(db: Session, user: CurrentUser, transaction_id: int) -> Transaction:
    transaction = db.get(Transaction, transaction_id)
    if transaction is None or transaction.account.user_id != user.id:
        raise HTTPException(status_code=404, detail="Buchung nicht gefunden")
    return transaction


@router.get("/", response_model=list[schemas.TransactionRead])
def list_transactions(
    account_id: int | None = None,
    category_id: int | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    query = select(Transaction).join(Account).where(Account.user_id == user.id)
    if account_id is not None:
        query = query.where(Transaction.account_id == account_id)
    if category_id is not None:
        query = query.where(Transaction.category_id == category_id)
    if date_from is not None:
        query = query.where(Transaction.booking_date >= date_from)
    if date_to is not None:
        query = query.where(Transaction.booking_date <= date_to)
    return db.scalars(query.order_by(Transaction.booking_date.desc(), Transaction.id.desc())).all()


@router.post("/", response_model=schemas.TransactionRead, status_code=201)
def create_transaction(
    data: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    own_account(db, user, data.account_id)
    own_category(db, user, data.category_id)
    transaction = Transaction(**data.model_dump())
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


@router.put("/{transaction_id}", response_model=schemas.TransactionRead)
def update_transaction(
    transaction_id: int,
    data: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    transaction = own_transaction(db, user, transaction_id)
    own_account(db, user, data.account_id)
    own_category(db, user, data.category_id)
    for key, value in data.model_dump().items():
        setattr(transaction, key, value)
    db.commit()
    db.refresh(transaction)
    return transaction


@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    db.delete(own_transaction(db, user, transaction_id))
    db.commit()


@router.post("/{transaction_id}/receipt")
def upload_receipt(
    transaction_id: int,
    file: UploadFile,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    todo()
