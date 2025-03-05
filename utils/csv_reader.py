import os
import platform
import re

import pandas as pd

from core.config import settings
from core.exceptions import NotFoundException


def clean_quantity(value):
    if pd.isna(value):
        return value
    value = str(value).strip()

    if re.match(r">\d+", value):
        return int(value[1:])
    elif re.match(r"<\d+", value):
        return int(value[1:])
    elif re.match(r"\d+-\d+", value):
        return int(value.split("-")[1])
    elif value.isdigit():
        return int(value)

    return value


def truncate_description(value):
    if pd.isna(value):
        return value
    return str(value)[:512]


def clean_text(value):
    return re.sub(r"[^a-zA-Z0-9]", "", value).upper() if isinstance(value, str) else value


def find_path_to_csv():
    current_os = platform.system()
    script_path = os.path.abspath(__file__)

    csv_script_path = ''
    if current_os == "Windows":

        script_path = script_path.split('\\')

        script_path = script_path[:-2]

        script_path.append('attachments')
        script_path.append(settings.email_config.sender_email)

        for path in script_path:
            csv_script_path += path + '\\'

        return csv_script_path

    if current_os == "Linux":
        script_path = script_path.split('/')

        script_path = script_path[:-2]

        script_path.append('attachments')
        script_path.append(settings.email_config.sender_email)

        for path in script_path:
            csv_script_path += path + '/'

        return csv_script_path


def data_frame_creation():
    csv_path = find_path_to_csv()
    try:
        csv_file = [f for f in os.listdir(csv_path) if f.endswith(".csv")]

        csv_file = csv_path + csv_file[0]
    except FileNotFoundError:
        raise NotFoundException("No csv file found")

    df = pd.read_csv(csv_file,
                     usecols=["Бренд", "Каталожный номер", "Описание", "Цена, руб.", "Наличие"],
                     sep=';',
                     decimal=',',
                     doublequote=False,
                     on_bad_lines="warn")

    column_mapping = {
        settings.column_mapping_config.vendor_mapping: "vendor",
        settings.column_mapping_config.number_mapping: "number",
        settings.column_mapping_config.description_mapping: "description",
        settings.column_mapping_config.price_mapping: "price",
        settings.column_mapping_config.count_mapping: "count",
    }

    df = df.rename(columns=column_mapping)

    df['price'] = df['price'].replace({',': '.'}, regex=True).astype(float)
    df["count"] = df["count"].apply(clean_quantity)
    df['count'] = df['count'].astype(int)
    df["search_vendor"] = df["vendor"].apply(clean_text)
    df["search_number"] = df["number"].apply(clean_text)
    df["description"] = df["description"].apply(truncate_description)

    return df
