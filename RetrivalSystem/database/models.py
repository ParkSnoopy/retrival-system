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


class Article(models.Model):
    
    url = models.CharField(blank=True, null=False, max_length=1024)
    title = models.CharField(blank=False, null=False, max_length=1024)
    date = models.DateField(blank=True, null=True)
    source = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField(blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    
    
    def __str__(self):
        return (
            "  << Article >>" + "\t"
            f"URL - {self.url}" + "\t"
            f"TITLE - {self.title}" + "\t"
            f"DATE - {self.date}" + "\t"
            f"FROM - {self.source}" + "\t"
            f"CATEGORY - {self.category}"
        )
