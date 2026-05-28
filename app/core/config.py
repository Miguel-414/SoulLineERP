from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int = 3306
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # App
    PROJECT_NAME: str = "Control Inventario API"
    API_V1_STR: str = "/api/v1"

    # Administrador maestro — se crea automáticamente si la BD está vacía.
    # Cambia estas credenciales en .env antes del primer despliegue.
    MASTER_ADMIN_USERNAME: str = "superadmiN"
    MASTER_ADMIN_PASSWORD: str = "Admin1234!"
    MASTER_ADMIN_EMAIL: str = "admin@soulline.com"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8')


settings = Settings()
