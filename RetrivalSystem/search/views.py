from django.shortcuts import render
from django.conf import settings

from .filterer import retrieve, process_article_content
from database.models import Article, Organization

# Create your views here.


def home(request, searchinput:str):
    
    if request.method == "POST":
        searchinput = request.POST['searchinput']
    
    results, counts = retrieve(searchinput)
    
    return render(request, 'search/index.html', {
        'searchinput': searchinput, 
        'results': results, 
        'counts': counts, 
    })


def details(request, article_pk:int):
    try:
        article = Article.objects.get( pk = article_pk )
        return render(request, 'search/details.html', {
            'exist': True, 
            'url': article.url, 
            'title': article.title, 
            'contents': process_article_content(article.content), 
            'source': article.source.name, 
            'date': article.date.strftime(settings.ZH_STRFTIME_FMT), 
        })
    except Article.DoesNotExist:
        return render(request, 'search/details.html', {
            'exist': False, 
            'article': None, 
        })