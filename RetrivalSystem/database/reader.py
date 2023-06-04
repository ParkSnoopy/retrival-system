# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 16:16:29 2023

@author: admin
"""

from django.conf import settings

from .local_option import LOCAL_OPTION
from .models import Article, Category, Organization

import csv


def url_to_category(url):
    slugs = url.split("gov.cn/")[1].split("/")
    for slug in slugs:
        if len(slug) == 4:
            return slug
    return slug[0]


def read_and_create_from(filename):
    
    # CSV FILE PATH
    data_path = settings.BASE_DIR / LOCAL_OPTION["DATA_DIR"] / filename
    
    with open( data_path, encoding='utf-8' ) as file:
        reader = csv.reader(file)
        
        # if read successfully, flush DB
        Article.objects.all().delete()
        Category.objects.all().delete()
        Organization.objects.all().delete()
        
        # CSV EFFECTIVE DATA FORMAT
        URL, title, date, source, article, *_ = next(reader)
        
        for row in reader:
            URL, title, date, source, article, *_ = row
            # article = process_article_content( article )
            
            organization, _ = Organization.objects.get_or_create( name = source )
            category, _ = Category.objects.get_or_create( name = url_to_category(URL) )
            
            article = Article.objects.create(
                url=URL, 
                title=title, 
                date=date, 
                source=organization, 
                content=article, 
                category=category, 
            )
            
            # print(f"\n  {article.pk} - \n    {article}\n")