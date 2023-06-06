from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError

from .filterer import (
    boolean_retrieve, 
    process_article_content, 
    build_query_ish, 
)
from database.models import Article

# Create your views here.



def home(request):
    if request.method == "POST":
        # print(f"\n  {request.POST = }\n")
        Post = dict(request.POST)
        try: Post.pop('csrfmiddlewaretoken')
        except KeyError: pass
        try: Post.pop('doSearch')
        except KeyError: pass
        # print(f"\n  {Post = }\n")
        
        searchinputs = ( request.POST[name] for name in filter(lambda x: 'searchinput' in x, Post.keys()) if request.POST[name] )
        
        try:
            do_search = True if request.POST['doSearch'] == '1' else False
        except MultiValueDictKeyError:
            do_search = True
        
        if not do_search:
            return redirect('homepage-home', status='0')
        else:
            if not any(searchinputs):
                return redirect('homepage-home', status='1')
        
        results = boolean_retrieve(dict(Post))
        
        return render(request, 'search/index.html', {
            'searchinput': build_query_ish(dict(Post)), 
            'results': results, 
            'counts': len(results), 
        })
    
    return redirect('homepage-home', status='0')


def details(request, article_pk:int):
    try:
        article = Article.objects.get( pk = article_pk )
        return render(request, 'search/details.html', {
            'exist': True, 
            'article': article, 
            'contents': process_article_content(article.content), 
            'date': article.date.strftime(settings.STRFTIME_FORMAT), 
        })
    except Article.DoesNotExist:
        return render(request, 'search/details.html', {
            'exist': False, 
            'article': None, 
        })



































































