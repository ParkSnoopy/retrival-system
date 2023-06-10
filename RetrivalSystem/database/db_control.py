# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 16:16:29 2023

@author: admin
"""

from django.conf import settings

from localutils.normalizer.main import zh_extract_tags, zh_normalize
from .local_option import LOCAL_OPTION
from .models import Article, Category, Organization, Region#, Tag, PrimaryTags, SecondaryTags

import csv
from datetime import date as datetime_date



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
        # Tag.objects.all().delete()
        # PrimaryTags.objects.all().delete()
        # SecondaryTags.objects.all().delete()
        
        # CSV EFFECTIVE DATA FORMAT
        # Column1	url	title	date	source	article	indexno	doc_no	category	region
        *_, url, title, date, source, content, indexno, docno, category, region = next(reader)
        i = 0
        print('\n')
        for row in reader:
            print(f"  creating row no.{i} ...", end="\r")
            i += 1
            n, url, title, date, source, content, indexno, docno, category, region = row
            # print(f" processing row {n} ...")
            date = tuple(int(n) for n in date.split('/'))
            date = datetime_date(date[2], date[0], date[1])
            # content = process_article_content( content )
            
            organization, _ = Organization.objects.get_or_create( name = ( source or "" ) )
            category, _ = Category.objects.get_or_create( name = ( category or "其他" ) )
            region, _ = Region.objects.get_or_create( name = ( region or "" ) )
            
            # pri_tags = PrimaryTags.objects.create()
            # sec_tags = SecondaryTags.objects.create()
            
            article = Article.objects.create(
                url = url, 
                title = title, 
                date = date, 
                source = organization, 
                content = content, 
                indexno = indexno, 
                documentno = docno, 
                category = category, 
                region = region, 
                # pri_tags = pri_tags, 
                # sec_tags = sec_tags, 
            )
            
            pri_tags, sec_tags = extract_tags(article)
            
            for tagname in pri_tags:
                # tag, _ = Tag.objects.get_or_create( name = tagname )
                # article.pri_tags.tags.add( tag )
                article.pri_tags.append( tagname )
            for tagname in sec_tags:
                # tag, _ = Tag.objects.get_or_create( name = tagname )
                # article.sec_tags.tags.add( tag )
                article.sec_tags.append( tagname )
            
            article.save()
            
            # print(f"\n\n  object no.{article.pk} has created and saved\n\n{article}\n")
        print('\n')
    # update FULLDATAS
    FULLDATAS = Article.objects.all()


def url_to_category(url):
    slugs = url.split("gov.cn/")[1].split("/")
    for slug in slugs:
        if len(slug) == 4:
            return slug
    return slug[0]


def extract_tags(article: Article, pri_n=10, sec_n=10) -> [ list[str], list[str] ]:
    pri = zh_normalize(f"{article.category.name} {article.title}", _rm_nums=True)
    sec = zh_normalize(f"{article.content}", _rm_nums=True)
    pri_tags = zh_extract_tags(pri, topK=pri_n)
    sec_tags = zh_extract_tags(sec, topK=None)
    # if not sec_tags:
    #     pri_tags, sec_tags = pri_tags[:5], pri_tags[5:]
    # else:
    #     pri_tags = pri_tags[:5]
    sec_tags = list(filter(lambda tagname: tagname not in pri_tags, sec_tags))[:sec_n]
    
    return pri_tags, sec_tags


































