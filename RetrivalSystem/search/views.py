from django.shortcuts import render

from database.models import Categories, Article

from collections import namedtuple
article = namedtuple("article", ("pk", "category", "title", "content"))

# Create your views here.


def home(request, searchinput:str):
    
    results = retrieve(searchinput)
    
    return render(request, 'search/index.html', 
        {
            'searchinput': searchinput, 
            'results': results, 
        }
    )



def retrieve(searchinput):
    
    # some algorithm here
    
    filtered = Article.objects.all().values()
    results = []
    
    for each in filtered:
        results.append(
            article(
                each['id'], 
                Categories.objects.get( pk = each['category_id'] ).categoryname, 
                each['title'], 
                each['content'].split('\r\n')
            )
        )
    
    return results