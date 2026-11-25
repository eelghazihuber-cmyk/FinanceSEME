from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # Supabase -> Connect -> Session pooler
    database_url: str = "postgresql://user:passwort@localhost:5432/financesme"
    # Supabase -> Project Settings -> API
    supabase_url: str = ""
    # nur für Weg 1 (geheimer Schlüssel)
    supabase_jwt_secret: str = ""
    # Frontend-Adressen, die das Backend aufrufen dürfen
    cors_origins: list[str] = ["http://localhost:5173"]
    # Claude-API (console.anthropic.com). Leer = KI-Analyse ausgeschaltet
    anthropic_api_key: str = ""

    @property
    def sqlalchemy_url(self) -> str:
        """Supabase-Adressen beginnen mit postgresql://.
        Hier legen wir fest, welchen Treiber SQLAlchemy nimmt (psycopg)."""
        if self.database_url.startswith("postgresql://"):
            return "postgresql+psycopg://" + self.database_url[len("postgresql://"):]
        return self.database_url


settings = Settings()
