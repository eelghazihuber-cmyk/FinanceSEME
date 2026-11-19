"""Registrieren und Einloggen laufen über Supabase direkt vom Frontend.
Hier bleibt nur ein Endpunkt, der zeigt, wer eingeloggt ist."""

from fastapi import APIRouter, Depends

from app.deps import get_current_user
from app.schemas import CurrentUser

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me", response_model=CurrentUser)
def me(user: CurrentUser = Depends(get_current_user)):
    return user
