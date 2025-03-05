import os

from httpx import Client
from sqlalchemy.orm import Session
from starlette import status

from utils.csv_reader import find_path_to_csv

def test_query_insert_csv_to_table(test_client: Client, db: Session) -> None:
    response = test_client.post(
        "api/api_v1/dataframes/insert_email_to_db",
    )

    csv_path = find_path_to_csv()
    if os.path.exists(csv_path):
        assert response.status_code == status.HTTP_200_OK
    else:
        assert response.status_code == status.HTTP_404_NOT_FOUND

