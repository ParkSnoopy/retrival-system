from django.db import models

# Create your models here.



class Organization(models.Model):
    
    name = models.CharField(blank=False, null=False, max_length=1024)
    
    def __str__(self):
        return f"{self.pk} - {self.name}"


class Category(models.Model):
    
    name = models.CharField(blank=False, null=False, max_length=1024)
    
    def __str__(self):
        return f"{self.pk} - {self.name}"


class Region(models.Model):
    
    name = models.CharField(blank=True, null=True, max_length=1024)
    
    def __str__(self):
        return f"{self.pk} - {self.name}"


class Article(models.Model):
    
    # url, title, date, source, article, indexno, docno, category, region
    
    url = models.CharField(blank=True, null=False, max_length=1024)
    title = models.CharField(blank=False, null=False, max_length=1024)
    date = models.DateField(blank=True, null=True)
    source = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField(blank=False, null=False)
    indexno = models.CharField(blank=True, null=True, max_length=1024)
    documentno = models.CharField(blank=True, null=True, max_length=1024)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    
    
    def __str__(self):
        return (
            "  << Article >>" + "\t"
            f"URL - {self.url}" + "\t"
            f"TITLE - {self.title}" + "\t"
            f"DATE - {self.date}" + "\t"
            f"FROM - {self.source}" + "\t"
            f"INDEX_NO - {self.indexno}" + "\t"
            f"DOCUMENT_NO - {self.documentno}" + "\t"
            f"CATEGORY - {self.category}" + '\t'
            f"REGION - {self.region}"
        )
