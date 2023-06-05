from django.shortcuts import render
from django.conf import settings

from .filterer import retrieve, process_article_content
from database.models import Article, Organization

from typing import Final

# Create your views here.


FULLDATAS: Final = Article.objects.all()

def home_yly(request):
    if request.method == "GET":
        column = request.GET.get('column')
        searchinput = request.GET.get('searchinput')
        
        # print(f"\n  {column = }\n  {searchinput = }\n")
        if not column and not searchinput:
            return render(request, 'search_others/yly.html', {
                'searchinput': searchinput, 
                'results': None, 
                'counts': 0, 
                
                'fulldatas': FULLDATAS, 
                'fulldatas_len': len(FULLDATAS), 
            })
        
        # print("\n  Retrieve\n")
        
        results, counts = retrieve(searchinput, _yly=True)
        
        # print(f"\n  {results = }\n  {counts = }\n")
        
        return render(request, 'search_others/yly.html', {
            'searchinput': searchinput, 
            'results': results, 
            'counts': counts, 
            
            'fulldatas': FULLDATAS, 
            'fulldatas_len': len(FULLDATAS), 
        })



