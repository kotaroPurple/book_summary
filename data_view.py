
import argparse

import plotly.express as px

from core.data_keeper import read_book_info


def _ndc_to_string(ndc: int) -> str:
    if ndc == 4:  # NOQA
        return '理学'
    elif ndc == 5:  # NOQA
        return '工学'
    else:
        return 'None'


def main() -> None:
    parser = argparse.ArgumentParser(description='merge files')
    parser.add_argument('datapath', default='')

    args = parser.parse_args()

    load_df = read_book_info(args.datapath)
    df = load_df.drop(columns=['title'])
    df['genre'] = df['ndc'].apply(_ndc_to_string)

    #
    # 出版社 (publisher) と出版年 (year) ごとに件数をカウント
    #
    publisher_df = df.groupby(['publisher', 'year']).size().reset_index(name='publication_count')

    fig = px.bar(
        publisher_df, x='year', y='publication_count',
        color='publisher', barmode='stack')

    fig.show()

    #
    # 理学 (ndc=4), 工学 (ndc=5) の出版数
    #
    ndc_df = df.groupby(['genre', 'year']).size().reset_index(name='publication_count')

    fig = px.bar(
        ndc_df, x='year', y='publication_count',
        color='genre', barmode='stack')

    fig.show()

    #
    # 年ごとの価格を表示
    #
    median_price = df.groupby('year')['price'].median().reset_index()
    fig = px.line(median_price, x='year', y='price', markers=True)

    fig.show()


if __name__ == "__main__":
    main()
