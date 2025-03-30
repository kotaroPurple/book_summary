
import argparse
from pathlib import Path

import pandas as pd

from core.data_keeper import read_book_info
from core.util import ColumnName


def main() -> None:
    parser = argparse.ArgumentParser(description='merge files')
    parser.add_argument('dir', default='')
    parser.add_argument('resultpath', default='')

    args = parser.parse_args()

    # main
    dirpath = args.dir
    p_dir = Path(dirpath)

    merged_df = None
    for p_file in p_dir.iterdir():
        sub_df = read_book_info(str(p_file))
        if sub_df.empty is False:
            # 重複を消す
            sub_df = sub_df.drop_duplicates(
                subset=[ColumnName.title, ColumnName.year, ColumnName.publisher])
            # 統合
            if merged_df is not None:
                merged_df = pd.concat((merged_df, sub_df), ignore_index=True)
            else:
                merged_df = sub_df

    if merged_df is None:
        return

    # save as parquet
    merged_df = merged_df.reset_index()
    merged_df.to_parquet(args.resultpath)

    load_df = read_book_info(args.resultpath)
    print(load_df.sample(5))


if __name__ == "__main__":
    main()
