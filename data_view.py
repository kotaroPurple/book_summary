
import argparse
from pathlib import Path

import pandas as pd
import plotly.express as px

from core.data_keeper import read_book_info


def main() -> None:
    parser = argparse.ArgumentParser(description='merge files')
    parser.add_argument('datapath', default='')

    args = parser.parse_args()

    load_df = read_book_info(args.datapath)
    df = load_df.drop(columns=['title', 'ndc', 'price'])

    # 出版社 (publisher) と出版年 (year) ごとに件数をカウント
    result = df.groupby(['publisher', 'year']).size().reset_index(name='publication_count')

    # Plotly Express で出版社ごとの時系列推移をプロット
    # fig = px.line(
    #     result,
    #     x='year',
    #     y='publication_count',
    #     color='publisher',
    #     markers=True,
    #     title='出版社別の出版件数の時系列推移',
    #     labels={'year': '出版年', 'publication_count': '出版件数', 'publisher': '出版社'}
    # )

    fig = px.bar(
        result, x='year', y='publication_count',
        color='publisher', barmode='stack')

    fig.show()


if __name__ == "__main__":
    main()
