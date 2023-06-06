# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 16:16:29 2023

@author: admin
"""

from django.conf import settings

from .local_option import LOCAL_OPTION
from .models import Article, Category, Organization, Region

import csv


def url_to_category(url):
    slugs = url.split("gov.cn/")[1].split("/")
    for slug in slugs:
        if len(slug) == 4:
            return slug
    return slug[0]

FULLDATAS = Article.objects.all()
def read_and_create_from(filename):
    global FULLDATAS
    
    # CSV FILE PATH
    data_path = settings.BASE_DIR / LOCAL_OPTION["DATA_DIR"] / filename
    
    with open( data_path, encoding='utf-8' ) as file:
        reader = csv.reader(file)
        
        # if read successfully, flush DB
        Article.objects.all().delete()
        Organization.objects.all().delete()
        Category.objects.all().delete()
        Region.objects.all().delete()
        
        # default values
        o = Organization.objects.create( name = "" )
        c = Category.objects.create( name = "其他" )
        r = Region.objects.create( name = "" )
        
        # CSV EFFECTIVE DATA FORMAT
        *_, url, title, date, source, article, indexno, docno, category, region = next(reader)
        for row in reader:
            # print(f"\n  {row = }\n")
            _, url, title, date, source, article, indexno, docno, category, region = row
            # article = process_article_content( article )
            
            organization, _ = Organization.objects.get_or_create( name = source ) if source else ( o, False )
            category, _ = Category.objects.get_or_create( name = category ) if category else ( c, False )
            region, _ = Region.objects.get_or_create( name = region ) if region else ( r, False )
            
            article = Article.objects.create(
                url = url, 
                title = title, 
                date = date, 
                source = organization, 
                content = article, 
                indexno = indexno, 
                documentno = docno, 
                category = category, 
                region = region, 
            )
            
            # print(f"\n  {article.pk} - \n    {article}\n")
    
    FULLDATAS = Article.objects.all()
