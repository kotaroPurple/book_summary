
from dataclasses import dataclass, asdict

import pandas as pd

from core.extractor import BookInfo
from core.util import ColumnName


@dataclass
class ValidInfo:
    title: str|None
    price: int|None
    year: int|None
    publisher: str|None
    ndc: int|None


def _convert_book_info(info: BookInfo) -> ValidInfo:
    title = info.title
    price = info.price if info.price >= 1 else None
    year = info.year if info.year >= 1 else None
    publisher = info.publisher if info.publisher else None
    ndc = info.ndc if info.ndc >= 0 else None
    return ValidInfo(title=title, price=price, year=year, publisher=publisher, ndc=ndc)


def book_list_to_dataframe(book_list: list[BookInfo]) -> pd.DataFrame:
    title_list = []
    price_list = []
    year_list = []
    publisher_list = []
    ndc_list = []

    # dataframe
    for book_info in book_list:
        info = _convert_book_info(book_info)
        title_list.append(info.title)
        price_list.append(info.price)
        year_list.append(info.year)
        publisher_list.append(info.publisher)
        ndc_list.append(info.ndc)

    data_dict = {
        ColumnName.title: title_list,
        ColumnName.price: price_list,
        ColumnName.year: year_list,
        ColumnName.publisher: publisher_list,
        ColumnName.ndc: ndc_list}

    return pd.DataFrame(data_dict)


def read_book_info(filepath: str) -> pd.DataFrame:
    # title,price,year,publisher,ndc
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath, encoding='utf-8')
    elif filepath.endswith('.parquet'):
        df = pd.read_parquet(filepath)
    else:
        return pd.DataFrame({})

    # check columns
    correct_columns = list(asdict(ColumnName()).values())
    if set(correct_columns).issubset(set(df.columns)) is False:
        return pd.DataFrame({})

    # output
    return df.filter(items=correct_columns)


if __name__ == '__main__':
    # main()
    pass
