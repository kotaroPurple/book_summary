
import xml.etree.ElementTree as ET

import requests


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


def parse_contents(contents: bytes) -> None:
    # <item> タグに出版情報がある
    root = ET.fromstring(contents)
    items = root.findall('.//item')
    if not items:
        return None

    results = []
    for item in items:
        record = _parse_record(item)
        results.append(record)
    print(results)


def _parse_record(item):
    # 名前空間の定義。実際のレスポンスに合わせて調整してください。
    ns = {'dc': 'http://purl.org/dc/elements/1.1/'}

    # 各要素を抽出
    title_elem = item.find('./dc:title', ns)
    publisher_elem = item.find('./dc:publisher', ns)
    date_elem = item.find('./dc:date', ns)
    return (title_elem.text, publisher_elem.text, date_elem.text)

    # # 名前空間の定義。実際のレスポンスに合わせて調整してください。
    # ns = {'dc': 'http://purl.org/dc/elements/1.1/'}

    # # 各要素を抽出
    # title_elem = item.find('./dc:title', ns)
    # publisher_elem = item.find('./dc:publisher', ns)
    # date_elem = item.find('./dc:date', ns)
    # subject_elem = item.find('./dc:subject', ns)  # 分類・主題情報

    # title = title_elem.text if title_elem is not None else "タイトル不明"
    # publisher = publisher_elem.text if publisher_elem is not None else "不明"

    # # 出版年は先頭4文字（"YYYY"形式）で抽出
    # year = None
    # if date_elem is not None and date_elem.text and len(date_elem.text) >= 4:
    #     try:
    #         year = int(date_elem.text[:4])
    #     except ValueError:
    #         year = None

    # # 分類情報については、今回はdc:subjectの内容をそのまま利用（複数ある場合は必要に応じて条件分岐してください）
    # classification = subject_elem.text if subject_elem is not None else "その他"

    # return (publisher, classification, year, title)


if __name__ == '__main__':
    NDL_URL = 'https://iss.ndl.go.jp/api/opensearch'
    query = make_query(publisher='培風館', year_from=2023, year_until=2023)
    content = fetch_ndl_data(NDL_URL, query)
    if content is not None:
        parse_contents(content)
