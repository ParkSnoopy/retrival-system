from django.shortcuts import render

from .filterer import retrieve
from database.db_control import FULLDATAS

# Create your views here.



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



