from fastapi import HTTPException
from sqlalchemy import insert
from sqlalchemy.orm import Session

from core.models import PriceItem


class DFRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def post_dataframe_to_db(self, dataframe):
        try:
            stmt = insert(PriceItem).values(dataframe.to_dict(orient="records"))
            self.session.execute(stmt)
            self.session.commit()
            return f'Data inserted into {str(PriceItem.__tablename__)}'
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_data_from_table_with_limit_and_offset(self, limit: int, offset: int):
        items = self.session.query(PriceItem).offset(offset).limit(limit).all()
        if len(items) == 0:
            raise HTTPException(status_code=404, detail='No data found')
        return items
