
# from nltk.corpus import stopwords; stopwords = set(stopwords.words('chinese'))

from django.conf import settings

from database.models import Article, Organization
from .zh_normalizer.main import zh_normalize, zh_jieba_cut
from .local_option import LOCAL_OPTION

from collections import namedtuple





ScoredObject = namedtuple("ScoredObject", ("obj", "score", ))
def filter_raw_objects(select_best, searchinput, objects, _return_minus=False) -> list[ScoredObject]:
    
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
    
    results.sort(key=lambda x: x.score, reverse=True)
    
    return results[:select_best], len(results), set((searchinput, *zh_jieba_cut( searchinput ), *n_searchinput, ))



def retrieve(searchinput, _yly=False):
    
    filtered, counts, targetwords = filter_raw_objects(
        None, 
        searchinput, 
        Article.objects.all(), 
        # _return_minus=_yly, 
    )
    
    results = [ 
        
        _article_parse(article, targetwords)
        for article in filtered
        
    ] if not _yly else [
        
        _yly_article_parse(article, targetwords)
        for article in filtered
        
    ]
    
    return results, counts



def process_article_content(content:str) -> list[str]:
    return content.replace("。", "。\r\n").replace("1.", "\r\n1.").split('\r\n')



ArticleTuple = namedtuple("ArticleTuple", ("pk", "date", "title", "content", "score", "source"))
def _article_parse(scoredobject: ScoredObject, targetwords=None):
    
    # CONTENT
    if len( scoredobject.obj.content ) > 100:
        content = str(scoredobject.obj.content)[:100] + " ..."
    else:
        content = str(scoredobject.obj.content)
    
    for word in targetwords:
        word = word.strip()
        if word:
            content = content.replace(word, f"<strong>{word}</strong>")
    
    return ArticleTuple(
        scoredobject.obj.pk, 
        scoredobject.obj.date.strftime(settings.STRFTIME_FORMAT), 
        str(scoredobject.obj.title), 
        content, 
        scoredobject.score, 
        str(scoredobject.obj.source.name), 
    )



YlyArticleTuple = namedtuple("YlyArticleTuple", ("url", "score", "title", "source", "date", "content"))
def _yly_article_parse(scoredobject: ScoredObject, targetwords=None):
    
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
    
    return YlyArticleTuple(
        str(scoredobject.obj.url), 
        scoredobject.score, 
        title, 
        str(scoredobject.obj.source.name), 
        str(scoredobject.obj.date.strftime(settings.STRFTIME_FORMAT)), 
        content, 
    )





































