
from dataclasses import dataclass


# column
@dataclass(frozen=True)
class ColumnName:
    title: str = 'title'
    price: str = 'price'
    year: str = 'year'
    publisher: str = 'publisher'
    ndc: str = 'ndc'


# 理工系出版社
# 参考: https://tam5917.hatenablog.com/entry/2021/05/11/181501
SCIENCE_PUBLISHERS = [
    '培風館',
    '裳華房',
    '朝倉書店',
    '共立出版',
    '森北出版',
    '丸善出版',
    '内田老鶴圃',
    '近代科学社',
    '数理工学社',
    'オーム社',
    'コロナ社',
    'サイエンス社',
    'オライリージャパン',
    '技術評論社',
    'インプレス社',
]

# '講談社サイエンティフィク',
# '講談社サイエンティフィク　情報科学専門書',
# '講談社サイエンティフィク　理工学専門書',

# 国会図書館 API URL
NDL_URL = 'https://iss.ndl.go.jp/api/opensearch'

# NDC
# 参考: https://www.libnet.pref.okayama.jp/shiryou/ndc/index.htm
NDC_LIST = [
    4,
    5,

    # 40,  # 自然科学
    # 41,  # 数学
    # 42,  # 物理学
    # 43,  # 化学
    # 44,  # 天文学、宇宙科学
    # 45,  # 地球科学、地学
    # 46,  # 生物科学、一般生物学
    # 47,  # 植物学
    # 48,  # 動物学
    # 49,  # 医学、薬学

    # 50,  # 技術、工学
    # 51,  # 建設工学、土木工学
    # 52,  # 建築学
    # 53,  # 機械工学、原子力工学
    # 54,  # 電気工学
    # 55,  # 海洋工学、船舶工学、兵器、軍事工学
    # 56,  # 金属工学、鉱山工学
    # 57,  # 化学工業
    # 58,  # 製造工業
    # 59,  # 家政学、生活科学
]

# 調べる年代
TARGET_YEARS = list(range(1950, 2025))
