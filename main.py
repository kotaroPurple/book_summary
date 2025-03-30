
import argparse
import itertools

from core.data_keeper import book_list_to_dataframe
from core.extractor import BookInfo, fetch_ndl_data, make_query, modify_book_info, parse_contents
from core.util import NDC_LIST, NDL_URL, SCIENCE_PUBLISHERS, TARGET_YEARS


def _dataheader_to_path(dataheader: str, publisher: str) -> str:
    return f'{dataheader}_{publisher}.csv'


def main() -> None:
    parser = argparse.ArgumentParser(description='extract or view')
    parser.add_argument('--extract', action='store_true')
    parser.add_argument('--dataheader', default='')  # dir/header (-> dir/header_{}.csv)

    args = parser.parse_args()

    # data extractor
    if args.extract:
        # 出版社ごとに保存
        for publisher in SCIENCE_PUBLISHERS:
            book_list: list[BookInfo] = []
            for ndc, year in itertools.product(NDC_LIST, TARGET_YEARS):
                print(publisher, year, ndc)
                query = make_query(
                    publisher=publisher, year_from=year, year_until=year, n_records=500, ndc=ndc)
                contents = fetch_ndl_data(NDL_URL, query)
                if contents is not None:
                    _book_list = parse_contents(contents)
                    _book_list = modify_book_info(
                        _book_list, ndc=ndc, publisher=publisher, year=year)
                    book_list.extend(_book_list)
            # data frame and save
            df = book_list_to_dataframe(book_list)
            savepath = _dataheader_to_path(args.dataheader, publisher)
            df.to_csv(savepath, index=False)
    # view data
    else:
        pass


if __name__ == "__main__":
    main()
