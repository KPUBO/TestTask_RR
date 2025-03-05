import os
import shutil

import pytest
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from core.models import Base, db_helper
from main import main_app
from table_test.data_insert import organizations_insert
from utils.csv_reader import find_path_to_csv

engine = create_engine(
    url=os.getenv('APP_CONFIG__TEST_DB__URL'),
    echo=False,
)


@pytest.fixture(scope='session')
def db_engine():
    with engine.begin() as conn:
        Base.metadata.create_all(bind=conn)

    yield engine

    with engine.begin() as conn:
        Base.metadata.drop_all(bind=conn)


@pytest.fixture(scope='session')
def db(db_engine):
    session = sessionmaker(
        bind=db_engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    with session() as session:
        session.begin()

        yield session

        session.rollback()

        for table in reversed(Base.metadata.sorted_tables):
            session.execute(text(f'TRUNCATE {table.name} CASCADE;'))
            session.commit()


@pytest.fixture(scope="module")
def test_client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    client = TestClient(main_app)
    main_app.dependency_overrides[db_helper.session_getter] = override_get_db
    yield client


@pytest.fixture(scope="module")
def rename_csv_dir():
    csv_path = find_path_to_csv()
    backup_path = csv_path.replace('attachments', 'test')
    if os.path.exists(csv_path):
        shutil.copytree(csv_path, backup_path)
        shutil.rmtree(csv_path)

    yield

    if os.path.exists(backup_path):
        shutil.move(backup_path, csv_path)


