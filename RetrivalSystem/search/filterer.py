
# from nltk.corpus import stopwords; stopwords = set(stopwords.words('chinese'))

from django.conf import settings

from database.models import Article, Organization
from .zh_normalizer.main import zh_normalize, zh_jieba_cut
from .local_option import LOCAL_OPTION

from collections import namedtuple; ArticleTuple = namedtuple("ArticleTuple", ("pk", "date", "title", "content", "score"))



def filter_objects_by_searchinput( select_best: int, searchinput: str, objects: list[dict] ) -> [list[dict] , int]:
    """
    Method for filter Article objects dictionary by user searchinput

    Parameters
    ----------
    select_best : int
        max number of instanse to return. None for return all.
    searchinput : str
        user search input.
    objects : list[dict]
        Article.objects.all().values(), which is <QuerySet list[dict]>.

    Returns
    -------
    ( list[dict] , int, Optional[tuple] )
        0 : filtered subset of objects.
        1 : length of all non-zero scored results.
        2 : if exists, anything customized.

    """
    
    n_searchinput = zh_normalize( searchinput )
    n_searchinput = set( zh_jieba_cut( n_searchinput ) )
    # r_searchinput = set( zh_jieba_cut( searchinput ) )
    # searchinput = filter( lambda word: word not in stopwords, searchinput )
    
    initlen = len( objects )
    # reversed for index consistensy even after 'objects.pop()'
    for i, obj in enumerate( objects[::-1] ):
        i = initlen - i - 1
        title, content, source = (
            obj['title'], 
            obj['content'], 
            str(Organization.objects.get( id = obj['source_id'] ).name), 
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
        # for word in r_searchinput:
        #     score += title.count( word )   * LOCAL_OPTION['raw']['title_match_score']
        #     score += content.count( word ) * LOCAL_OPTION['raw']['content_match_score']
        #     score += source.count( word )  * LOCAL_OPTION['raw']['source_match_score']
        #     score += date.count( word )    * LOCAL_OPTION['raw']['date_match_score']
        
        if score > 0:
            objects[i]['score'] = score
        else:
            # print(f"{score=}, pop {i} from length {len(objects)}")
            objects.pop(i)
    
    objects.sort(key=lambda x: x['score'], reverse=True)
    
    return objects[:select_best], len(objects), set((searchinput, *zh_jieba_cut( searchinput ), *n_searchinput, ))


def retrieve(searchinput):
    
    objects = list( Article.objects.all().values() )
    filtered, counts, targetwords = filter_objects_by_searchinput(None, searchinput, objects)
    
    results = []
    for article in filtered:
        
        content = article['content']
        if len( content ) > 100:
            content = content[:100]
            content += " ..."
        
        for word in targetwords:
            word = word.strip()
            if word:
                content = content.replace(word, f"<strong>{word}</strong>")
        
        results.append(
            ArticleTuple(
                article['id'], 
                article['date'].strftime(settings.STRFTIME_FORMAT), 
                article['title'], 
                content, 
                article['score'], 
            )
        )
    
    return results, counts


def process_article_content(content:str) -> list[str]:
    return content.replace("。", "。\r\n").replace("1.", "\r\n1.").split('\r\n')
