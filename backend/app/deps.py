from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.models import Account, Category
from app.schemas import CurrentUser
from app.services.auth_service import TokenVerifier

bearer = HTTPBearer()
verifier = TokenVerifier()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer)) -> CurrentUser:
    """Liest das Token aus dem Header "Authorization: Bearer <Token>" und prüft es."""
    return verifier.verify(credentials.credentials)


def own_account(db: Session, user: CurrentUser, account_id: int) -> Account:
    """Konto laden, aber nur wenn es dem eingeloggten Nutzer gehört."""
    account = db.get(Account, account_id)
    if account is None or account.user_id != user.id:
        raise HTTPException(status_code=404, detail="Konto nicht gefunden")
    return account


def own_category(db: Session, user: CurrentUser, category_id: int | None) -> Category | None:
    if category_id is None:
        return None
    category = db.get(Category, category_id)
    if category is None or category.user_id != user.id:
        raise HTTPException(status_code=404, detail="Kategorie nicht gefunden")
    return category
