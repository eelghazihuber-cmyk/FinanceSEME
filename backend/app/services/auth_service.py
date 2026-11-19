import jwt
from fastapi import HTTPException
from jwt import PyJWKClient

from app.config import settings
from app.schemas import CurrentUser

# Supabase unterschreibt Tokens entweder mit einem geheimen Schlüssel (HS256)
# oder mit einem privaten Schlüssel (ES256/RS256), dessen öffentlicher Teil
# unter /auth/v1/.well-known/jwks.json abrufbar ist.
ASYMMETRIC = ("ES256", "RS256")


class TokenVerifier:
    """Prüft die Tokens, die Supabase beim Login ausstellt."""

    def __init__(self):
        self.jwt_secret = settings.supabase_jwt_secret
        self.jwks = (
            PyJWKClient(f"{settings.supabase_url}/auth/v1/.well-known/jwks.json", cache_keys=True)
            if settings.supabase_url
            else None
        )

    def _key_for(self, token: str, alg: str):
        if alg == "HS256" and self.jwt_secret:
            return self.jwt_secret
        if alg in ASYMMETRIC and self.jwks is not None:
            return self.jwks.get_signing_key_from_jwt(token).key
        raise jwt.InvalidTokenError(f"Algorithmus {alg} nicht konfiguriert")

    def verify(self, token: str) -> CurrentUser:
        try:
            alg = jwt.get_unverified_header(token).get("alg", "")
            payload = jwt.decode(
                token,
                self._key_for(token, alg),
                algorithms=[alg],
                audience="authenticated",  # nur Tokens eingeloggter Nutzer
            )
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Token ungültig oder abgelaufen")
        return CurrentUser(id=payload["sub"], email=payload.get("email"))
