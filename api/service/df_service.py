from sqlalchemy.orm import Session

from api.repository.df_repository import DFRepository


class DFService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = DFRepository(session)

    def post_dataframe_to_db(self, dataframe):
        return self.repository.post_dataframe_to_db(dataframe)

    def get_data_from_table_with_limit_and_offset(self, limit, offset):
        return self.repository.get_data_from_table_with_limit_and_offset(limit, offset)
