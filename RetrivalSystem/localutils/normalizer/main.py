
from .cn_tn import TextNorm

import re
import jieba
import jieba.analyse as analyse

from django.conf import settings

jieba.dt.tmp_dir = settings.BASE_DIR / 'cache' / 'jieba'

analyse.set_stop_words('localutils/normalizer/STOPWORDS.txt')

normalizer = TextNorm(
    to_lower = True,
    remove_fillers = True,
    remove_erhua = True,
    remove_space = True,
    cc_mode = 't2s',
)


def zh_normalize(text: str, _rm_nums=False) -> str:
    if _rm_nums:
        text = re.sub("[0-9]+", "", text)
    text = text.strip()
    text = normalizer(text)
    return text


def zh_jieba_cut(text: str) -> list[str]:
    return [ word.strip() for word in jieba.cut(text) if word.strip() ]


def zh_extract_tags(text: str, topK=10) -> list[str]:
    return analyse.extract_tags(text, topK=topK)


def count(substring, fullstring):
    return len( re.findall(re.compile(substring), fullstring) )
