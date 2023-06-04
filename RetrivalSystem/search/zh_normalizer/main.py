
from .cn_tn import TextNorm
import jieba


normalizer = TextNorm(
    to_lower = True,
    remove_fillers = True,
    remove_erhua = True,
    remove_space = True,
    cc_mode = 't2s',
)


def zh_normalize(text: str) -> str:
    text = text.strip()
    text = normalizer(text)
    return text


def zh_jieba_cut(text: str) -> list[str]:
    return jieba.cut(text)
