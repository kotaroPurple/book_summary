
import re
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from xml.etree.ElementTree import Element

import requests


@dataclass
class BookInfo:
    title: str = ''
    price: int = -1
    year: int = -1
    publisher: str = ''
    ndc: int = -1

    def is_valid(self) -> bool:
        return len(self.title) >= 1


def _price_string_to_integer(price_str: str) -> int|None:
    if price_str == '':
        return None
    # 全角数字を半角に変換する
    normalized = unicodedata.normalize('NFKC', price_str)
    # 数字以外の文字を削除する（コンマや「円」など）
    digits = re.sub(r'\D', '', normalized)
    # 整数に変換する
    if digits:
        return int(digits)
    else:
        return None


def _date_string_to_year(date_str: str) -> int|None:
    # 出版年は先頭4文字（"YYYY"形式）で抽出
    year_digits = 4
    year = None
    if date_str is not None and date_str and len(date_str) >= year_digits:
        try:
            year = int(date_str[:year_digits])
        except ValueError:
            year = None
    return year


def make_query(
        publisher: str = '', ndc: int = -1, year_from: int = -1, year_until: int = -1,
        n_records: int = 200) -> dict:
    query = {}
    if publisher != '':
        query['publisher'] = publisher
    if ndc >= 0:
        query['ndc'] = ndc
    # from, until は値を含む
    # 2025年のみを取得する時は from=2025, until=2025
    if year_from >= 0:
        query['from'] = year_from
    if year_until >= 0:
        query['until'] = year_until
    if n_records >= 0:
        query['cnt'] = n_records
    return query


def fetch_ndl_data(ndl_url: str, query: dict) -> bytes|None:
    if not query:
        return None

    response = requests.get(ndl_url, params=query)
    if response.status_code == requests.codes.ok:
        return response.content
    else:
        return None


def parse_contents(contents: bytes) -> list[BookInfo]:
    # <item> タグに出版情報がある
    root = ET.fromstring(contents)
    items = root.findall('.//item')
    if not items:
        return []

    results = []
    for item in items:
        record = _parse_record(item)
        if record.is_valid():
            results.append(record)
    return results


def _parse_record(item: Element) -> BookInfo:
    ns = {'dc': 'http://purl.org/dc/elements/1.1/'}

    # 各要素を抽出
    title_elem = item.find('./dc:title', ns)
    publisher_elem = item.find('./dc:publisher', ns)
    date_elem = item.find('./dc:date', ns)

    # タイトルがないときは向こうを返す
    if title_elem is None:
        return BookInfo()

    # 出版社
    publisher = ''
    if publisher_elem is not None:
        publisher = publisher_elem.text

    # 年数を取得
    if date_elem is None:
        year = None
    else:
        year = _date_string_to_year(str(date_elem.text))

    if year is None:
        year = -1

    # 値段を取得
    price = None
    for child in item:
        if 'price' in child.tag:
            price_str = child.text
            if price_str is None:
                continue
            value = _price_string_to_integer(price_str)
            if isinstance(value, int):
                price = value
                break

    if price is None:
        price = -1

    # output
    result = BookInfo(title=str(title_elem.text), price=price, publisher=str(publisher), year=year)
    return result


def modify_book_info(
        book_list: list[BookInfo], ndc: int|None = None, publisher: str|None = None,
        year: int|None = None) -> list[BookInfo]:
    # update ndc
    if ndc is not None:
        for book_info in book_list:
            book_info.ndc = ndc

    # update publisher
    if publisher is not None:
        for book_info in book_list:
            book_info.publisher = publisher

    # update year
    if year is not None:
        for book_info in book_list:
            book_info.year = year

    return book_list


if __name__ == '__main__':
    NDL_URL = 'https://iss.ndl.go.jp/api/opensearch'
    query = make_query(publisher='培風館', year_from=1986, year_until=1986, n_records=500, ndc=41)
    content = fetch_ndl_data(NDL_URL, query)
    if content is not None:
        book_list = parse_contents(content)
        book_list = modify_book_info(book_list, ndc=41, publisher='hoge', year=None)
        print(book_list)
