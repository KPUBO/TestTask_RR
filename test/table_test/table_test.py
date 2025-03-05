from httpx import Client
from sqlalchemy import text
from sqlalchemy.orm import Session

from core.models import Base
from table_test.data_insert import organizations_insert


def test_query_insert_csv_to_table_200(test_client: Client, db: Session) -> None:
    organizations_insert(db)
    response = test_client.get(
        "api/api_v1/dataframes/items?limit=10&offset=0",
    )

    items = response.json()

    assert response.status_code == 200
    assert len(items) == 10
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(text(f'TRUNCATE {table.name} CASCADE;'))
        db.commit()


def test_query_insert_csv_to_table_404(test_client: Client, db: Session) -> None:
    response = test_client.get(
        "api/api_v1/dataframes/items?limit=10&offset=0",
    )

    assert response.status_code == 404
