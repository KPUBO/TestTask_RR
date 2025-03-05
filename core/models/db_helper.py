from requests import Session
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings


class DatabaseHelper:
    def __init__(
            self,
            url: str,
            echo: bool,
            echo_pool: bool = False,
            pool_size: int = 5,
            max_overflow: int = 10,
    ) -> None:
        self.engine: Engine = create_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: sessionmaker[Session] = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def dispose(self):
        self.engine.dispose()

    def session_getter(self):
        with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    url=str(settings.db.url),
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
    echo=settings.db.echo
)
