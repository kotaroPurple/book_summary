
import xml.etree.ElementTree as ET
from collections import Counter

import matplotlib.pyplot as plt
import requests


# 国会図書館 API からデータを取得する関数
def fetch_ndl_data(query, records=100):
    # ここでは、国会図書館サーチ API のエンドポイント例を使用しています。
    url = "https://iss.ndl.go.jp/api/opensearch"
    params = {
        "q": query,       # 検索キーワード。例：「理工」
        "cnt": records    # 取得件数
        # 必要に応じてその他のパラメータ（出版年や分類コードでの絞り込みなど）を追加してください。
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.content
    else:
        print("データ取得エラー:", response.status_code)
        return None


# 取得した XML データから出版年を抽出する関数
def parse_publication_years(xml_data):
    root = ET.fromstring(xml_data)
    years = []
    # XML 内の名前空間を定義（実際のレスポンスに合わせて調整してください）
    ns = {'dc': 'http://purl.org/dc/elements/1.1/'}
    # 書誌情報の各レコードから出版年を取得
    for date_elem in root.findall('.//dc:date', ns):
        date_text = date_elem.text
        if date_text and len(date_text) >= 4:
            try:
                # 先頭4文字を年として整数化（"YYYY"形式が前提）
                year = int(date_text[:4])
                years.append(year)
            except ValueError:
                continue
    return years


# 出版年ごとの件数をグラフで表示する関数
def plot_year_trend(years):
    counter = Counter(years)
    years_sorted = sorted(counter.keys())
    counts = [counter[year] for year in years_sorted]

    plt.figure(figsize=(10, 6))
    plt.bar(years_sorted, counts)
    plt.xlabel("Year")
    plt.ylabel("Counts")
    plt.title("time series")
    plt.xticks(years_sorted, rotation=45)
    plt.tight_layout()
    plt.show()


# メイン処理
if __name__ == "__main__":
    # 例として「理工」というキーワードで検索
    query = "理工"
    xml_data = fetch_ndl_data(query, records=200)
    if xml_data:
        print(xml_data.decode('utf-8'))
        years = parse_publication_years(xml_data)
        if years:
            plot_year_trend(years)
        else:
            print("出版年のデータが見つかりませんでした。")
