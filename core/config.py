from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic import PostgresDsn

from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str
    port: int

class EmailConfig(BaseModel):
    email: str
    password: str
    imap_server: str
    imap_port: str
    sender_email: str
    subject_keyword: str

class ColumnMappingConfig(BaseModel):
    vendor_mapping: str
    number_mapping: str
    description_mapping: str
    price_mapping: str
    count_mapping: str

class TestDatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool


class ApiV1Prefix(BaseModel):
    prefix: str = "/api_v1"
    users: str = '/users'


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool
    max_overflow: int = 10
    pool_size: int = 50

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    api: ApiPrefix = ApiPrefix()
    load_dotenv()
    run: RunConfig
    db: DatabaseConfig
    test_db: TestDatabaseConfig
    email_config: EmailConfig
    column_mapping_config: ColumnMappingConfig


settings = Settings()
