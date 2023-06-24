
# from nltk.corpus import stopwords; stopwords = set(stopwords.words('chinese'))

from django.conf import settings

from database.models import Article, Organization, Category, Region
from localutils.normalizer.main import zh_normalize, zh_jieba_cut
from .local_option import LOCAL_OPTION

from collections import namedtuple
import numpy as np


_allcolumns = ('url', "title", "date", "source_id", "content", "indexno", "documentno", "category_id", "region_id")
ScoredObject = namedtuple("ScoredObject", ("obj", "score", ))
ArticleTuple = namedtuple("ArticleTuple", ("pk", "title", "date", "source", "content", "indexno", "documentno", "category", "region", "score", "tags", ))
YlyArticleTuple = namedtuple("YlyArticleTuple", ("url", "score", "title", "source", "date", "content"))
_searchinputcolumns = ('andor', 'column', 'searchinput', )
SearchInput = namedtuple("SearchInput", _searchinputcolumns)
SearchResult = namedtuple("SearchResult", ('andor', 'searchinput', 'result', ))


def _reverse_result(scoredobjects: list[ScoredObject]) -> list[ScoredObject]:
    obj_pks = set( scoredobject.obj.pk for scoredobject in scoredobjects )
    # print(f"\n  {obj_pks = } ({len(obj_pks)})\n")
    articles = Article.objects.all()
    # print(f"\n  {tuple(a.pk for a in articles) = } ({sum(1 for a in articles)})\n")
    articles = list(filter(lambda article: article.pk not in obj_pks, articles ))
    # print(f"\n  filtered {tuple(a.pk for a in articles) = } ({sum(1 for a in articles)})\n")
    return [
        ScoredObject(
            article, 
            1, 
        )
        for article in articles
    ]

def _filter_raw_objects(searchinput, objects, _return_minus=False, _not=False) -> list[ScoredObject]:
    n_searchinput = zh_normalize( searchinput )
    n_searchinput = set( zh_jieba_cut( n_searchinput ) )
    results = []
    for i, obj in enumerate( objects ):
        title, content, source = (
            str(obj.title), 
            str(obj.content), 
            str(obj.source.name), 
        )
        title = zh_normalize( title )
        content = zh_normalize( content )
        score = 0
        for word in n_searchinput:
            count = title.count( word )
            score += (
                count * LOCAL_OPTION['normalized']['match']['title']
                if count > 0 else
                LOCAL_OPTION['normalized']['mismatch']['title']
            )
            count = content.count( word )
            score += (
                count * LOCAL_OPTION['normalized']['match']['content']
                if count > 0 else
                LOCAL_OPTION['normalized']['mismatch']['content']
            )
            count = source.count( word )
            score += (
                count * LOCAL_OPTION['normalized']['match']['source']
                if count > 0 else
                LOCAL_OPTION['normalized']['mismatch']['source']
            )
        if score > 0 or _return_minus:
            results.append(
                ScoredObject(obj, score, )
            )
    if _not:
        results = _reverse_result(results)
    results.sort(key=lambda x: x.score, reverse=True)
    return results, len(results), set((searchinput, *zh_jieba_cut( searchinput ), *n_searchinput, ))

def retrieve(searchinput, _yly=False, _return_minus=False, _return_objects=False, _not=False) -> list[ArticleTuple] | list[ScoredObject]:
    filtered, counts, targetwords = _filter_raw_objects(
        searchinput, 
        Article.objects.all(), 
        _return_minus=_return_minus, 
        _not=_not, 
    )
    results = _article_parse(filtered, targetwords) if ( not _yly ) else _yly_article_parse(filtered, targetwords)
    if _return_objects:
        return results, counts, filtered
    return results, counts




def process_article_content(content:str) -> list[str]:
    return content.replace("。", "。\r\n").replace("1.", "\r\n1.").split('\r\n')

def _article_parse(scoredobjects: list[ScoredObject], targetwords=None) -> list[ArticleTuple]:
    results = []
    for scoredobject in scoredobjects:
        # CONTENT
        if len( scoredobject.obj.content ) > 100:
            content = str(scoredobject.obj.content)[:100] + " ..."
        else:
            content = str(scoredobject.obj.content)
        if targetwords:
            for word in targetwords:
                word = word.strip()
                if word:
                    content = content.replace(word, f"<strong>{word}</strong>")
        results.append(
            ArticleTuple( # ("pk", "title", "date", "source", "content", "indexno", "documentno", "category", "region", "score", )
                scoredobject.obj.pk, 
                str(scoredobject.obj.title), 
                scoredobject.obj.date.strftime(settings.STRFTIME_FORMAT), 
                str(scoredobject.obj.source.name), 
                content, 
                str(scoredobject.obj.indexno), 
                str(scoredobject.obj.documentno), 
                str(scoredobject.obj.category.name), 
                str(scoredobject.obj.region.name), 
                scoredobject.score, 
                "、".join( scoredobject.obj.sec_tags if scoredobject.obj.sec_tags else scoredobject.obj.pri_tags ), 
            )
        )
    return results

def _yly_article_parse(scoredobjects: list[ScoredObject], targetwords=None) -> list[YlyArticleTuple]:
    results = []
    for scoredobject in scoredobjects:
        # TITLE
        if len( scoredobject.obj.title ) > 20:
            title = str(scoredobject.obj.title)[:20] + " ..."
        else:
            title = str(scoredobject.obj.title)
        # CONTENT
        if len( scoredobject.obj.content ) > 60:
            content = str(scoredobject.obj.content)[:60] + " ..."
        else:
            content = str(scoredobject.obj.content)
        # STRONGIFY SEARCH WORDS
        for word in targetwords:
            word = word.strip()
            if word:
                content = content.replace(word, f"<strong>{word}</strong>")
        results.append(
            YlyArticleTuple(
                str(scoredobject.obj.url), 
                scoredobject.score, 
                title, 
                str(scoredobject.obj.source.name), 
                str(scoredobject.obj.date.strftime(settings.STRFTIME_FORMAT)), 
                content, 
            )
        )
    return results



'''
<option value="" selected></option>
<option value="链接">链接</option>
<option value="标题">标题</option>
<option value="日期">日期</option>
<option value="发文机构">发文机构</option>
<option value="正文">正文</option>
<option value="索引号">索引号</option>
<option value="发文字号">发文字号</option>
<option value="分类">分类</option>
<option value="地区">地区</option>
'''
COLUMN = {
    'source': 'source_id', 
    'category': 'category_id', 
    'region': 'region_id', 
}
ZH2EN = {
    'pri_tags': 'pri_tags', 
    'sec_tags': 'sec_tags',     
    '链接': 'url', 
    '标题': 'title', 
    '日期': 'date', 
    '发文机构': 'source', 
    '正文': 'content', 
    '索引号': 'indexno', 
    '发文字号': 'documentno', 
    '分类': 'category', 
    '地区': 'region', 
}
def _cleaned_column_name(column, _deep=True):
    if column in COLUMN.values():
        return column, True
    if column in ZH2EN.values():
        if column not in COLUMN.keys():
            return column, False
    else:
        column = ZH2EN[column]
    if _deep and column in COLUMN.keys():
        return COLUMN[column], True
    return column, False

MODEL = {
    'source_id': Organization, 
    'category_id': Category, 
    'region_id': Region, 
}
def _str(obj, column, is_foreignkey) -> str:
    column, is_foreignkey = _cleaned_column_name(column)
    content = obj.__dict__[column]
    if is_foreignkey:
        content = str(MODEL[column].objects.get(pk=content).name)
    elif column == 'date':
        content = content.strftime(settings.STRFTIME_FORMAT)
    else:
        content = str(content)
    return content

def _filter_raw_objects_on_column(column:str, searchinput:str, _not=False) -> list[ScoredObject]:
    searchinputs = zh_jieba_cut(searchinput)
    articles = Article.objects.all()
    column, is_foreignkey = _cleaned_column_name(column)
    results = []
    # print(f"    searching with {searchinputs=} {column=} {is_foreignkey=}")
    # if column in _allcolumns:   print("      NOT tags")
    # else:                       print("      IS  tags")
    for article in articles:
        if column in _allcolumns: # '_allcolumns' does not include 'pri_tags' and 'sec_tags'
            """
            NOT TAGS
            """
            count = 0
            for searchinput in searchinputs:
                content: str = _str(article, column, is_foreignkey)
                count += content.count(searchinput)
            if count > 0:
                results.append(
                    ScoredObject(article, count)
                )
        else:
            """
            IS TAGS
            """
            count = 0
            assert type(article.pri_tags) == type(article.sec_tags) == list, "not list"
            for searchinput in searchinputs:
                for tag in article.pri_tags:
                    if searchinput in tag:
                        count += 5
                for tag in article.sec_tags:
                    if searchinput in tag:
                        count += 2
            if count > 0:
                results.append(
                    ScoredObject(article, count)
                )
    if _not:
        results = _reverse_result(results)
    results.sort(key=lambda x: x.score, reverse=True)
    return results

def columnly_retrieve(column, searchinput, _return_objects=False, _not=False) -> list[ArticleTuple] | list[ScoredObject]:
    # print(f"  call '_filter_raw_objects_on_column()' with {column=} {searchinput=}")
    filtered: list[ScoredObject] = _filter_raw_objects_on_column(
        column, 
        searchinput, 
        _not=_not, 
    )
    results = _article_parse(filtered, searchinput)
    if _return_objects:
        return results, len(results), filtered
    return results, len(results)




def _int_to_str(n, paddings):
    return f"{n:0{paddings}d}"

def _pack_postdatas(postdatas) -> list[SearchInput]:
    results = []
    i = 0
    while postdatas:
        try:
            no = _int_to_str(i, 2)
            results.append(
                SearchInput(*(
                    postdatas.pop(f"{part}-{no}")[0]
                    for part in _searchinputcolumns
                ))
            )
            i += 1
        except KeyError:
            break
    return results

def _multicolumn_retrieve(postdatas) -> list[SearchResult]:
    postdatas = _pack_postdatas(postdatas)
    results = []
    for postdata in postdatas:
        is_not = ( postdata.andor == 'NOT' )
        if postdata.column != '':
            *_, filtered = columnly_retrieve(postdata.column, postdata.searchinput, _return_objects=True, _not=is_not)
        else:
            filtered = set()
            for column in ('pri_tags', 'sec_tags', ):
                *_, _filtered = columnly_retrieve(column, postdata.searchinput, _return_objects=True, _not=is_not)
                filtered.update(_filtered)
            filtered = list(filtered)
            filtered.sort(key=lambda so: so.score, reverse=True)
        # else:
        #     filtered = set()
        #     for column in _allcolumns:
        #         *_, _filtered = columnly_retrieve(column, postdata.searchinput, _return_objects=True, _not=is_not)
        #         filtered.update(_filtered)
        #     filtered = list(filtered)
        #     filtered.sort(key=lambda so: so.score, reverse=True)
        
        results.append(
            SearchResult(
                postdata.andor, 
                postdata.searchinput, 
                filtered, 
            )
        )
    return results

def _set_computation(results: list[SearchResult]) -> set[ScoredObject]:
    if len(results) == 1:
        return set( results[0].result )
    output = set( results[0].result )
    for result in results[1:]:
        if result.andor in ('AND', 'NOT', ):
            output = output & set( result.result )
        else:
            output = output | set( result.result )
    return output

def boolean_retrieve(postdatas) -> list[str: set]:
    results: list[SearchResult] = _multicolumn_retrieve(postdatas)
    results: set[ScoredObject] = _set_computation(results)
    results: list[ArticleTuple] = _article_parse(results)
    results.sort(key=lambda at: at.date, reverse=True)
    results.sort(key=lambda at: at.score, reverse=True)
    return results




# def _normalize(scores: list[int]) -> list[np.float64]:
#     scores = list(scores)
#     minn, maxx = np.min(scores), np.max(scores)
#     _max = maxx - minn
#     for i, score in enumerate(scores):
#         scores[i] = ( score - minn ) / _max
#     return scores

# def _normalize_scoredobjects(objects: list[ScoredObject]) -> list[ScoredObject]:
#     scores = ( obj.score for obj in objects )
#     results = [
#         ScoredObject(
#             objects[i].obj, 
#             score, 
#         )
#         for i, score in enumerate(_normalize(scores))
#     ]
#     return results

# def filter_based_on_cluster(objects: list[ScoredObject], _yly=False) -> list[ScoredObject]:
#     objects = _normalize_scoredobjects(objects)
#     objects.sort(key=lambda obj: obj.score, reverse=True)
#     before = 1.0
#     for i, obj in enumerate(objects):
#         if before - obj.score > LOCAL_OPTION['cluster']['distance']:
#             i -= 1
#             break
#         before = obj.score
#     i += 1
#     return objects[:i], i



ARITHMETIC_MAP = {
    'AND': '和', 
    'OR' : '或', 
    'NOT': '非', 
}
def _columnname_of(postdata):
    return postdata.column if postdata.column.strip() else '标签'
def build_query_ish(postdatas):
    postdatas: list[SearchInput] = _pack_postdatas(postdatas)
    column = column = _columnname_of(postdatas[0])
    buffer = f"( {column} = {postdatas[0].searchinput} )"
    for postdata in postdatas[1:]:
        column = _columnname_of(postdata)
        buffer += f" {ARITHMETIC_MAP[postdata.andor]} ( {column} = {postdata.searchinput} )"
    return buffer












































