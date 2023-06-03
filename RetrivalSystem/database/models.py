from django.db import models

# Create your models here.



class Categories(models.Model):
    
    categoryname = models.CharField(
        blank=False, null=False, max_length=1024, 
    )
    
    def __str__(self):
        return f"{self.pk} - {self.categoryname}"



class Article(models.Model):
    
    category = models.ForeignKey(
        Categories, 
        on_delete=models.CASCADE, 
    )
    title = models.CharField(
        blank=False, null=False, max_length=1024, 
    )
    content = models.TextField(
        blank=False, null=False, 
    )
    
    def __str__(self):
        return f"{self.title} ({str(self.category).split(' - ')[-1]}) - {self.content[:100]}"
