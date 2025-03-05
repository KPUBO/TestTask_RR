from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.service.df_service import DFService
from core.exceptions import NotFoundException, InvalidCredentialsException
from core.models import db_helper
from utils.csv_reader import data_frame_creation
from utils.email_downloader import download_message_attachments

router = APIRouter(
    prefix='/dataframes',
    tags=['DataFrames']
)


@router.get('/download_email')
def get_email():
    try:
        download_message_attachments()
        return f'Искомое письмо найдено, вложение скачано'
    except InvalidCredentialsException:
        raise HTTPException(status_code=401, detail='Email credentials in .env file are invalid')
    except NotFoundException:
        raise HTTPException(status_code=404, detail='Message not found')


@router.get('/items')
def get_data_from_table_with_limit_and_offset(
        limit: int = 10,
        offset: int = 0,
        session: Session = Depends(db_helper.session_getter)
):
    df_service = DFService(session)
    result = df_service.get_data_from_table_with_limit_and_offset(limit, offset)
    return result


@router.post('/insert_email_to_db')
def insert_email_to_db(
        session: Session = Depends(db_helper.session_getter)
):
    df_service = DFService(session)
    try:
        resp = df_service.post_dataframe_to_db(data_frame_creation())
        return resp
    except NotFoundException:
        raise HTTPException(status_code=404, detail='Email not found (try to execute "get_email" query)')
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
