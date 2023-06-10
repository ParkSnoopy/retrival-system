from django.db import models

# Create your models here.



# class Tag(models.Model):
    
#     name = models.CharField(blank=False, null=False, max_length=1024)
    
#     def __str__(self):
#         return f"{self.pk} - {self.name}"


# class PrimaryTags(models.Model):
    
#     tags = models.ManyToManyField(Tag, blank=True)
    
#     def __str__(self):
#         return f"{self.pk} - {self.str()}"
#     def str(self):
#         return f"[ {' & '.join( tag.name for tag in self.tags.all() )} ]"


# class SecondaryTags(models.Model):
    
#     tags = models.ManyToManyField(Tag, blank=True)
    
#     def __str__(self):
#         return f"{self.pk} - {self.str()}"
#     def str(self):
#         return f"[ {' & '.join( tag.name for tag in self.tags.all() )} ]"


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
    content = models.TextField(blank=True, null=True)
    indexno = models.CharField(blank=True, null=True, max_length=1024)
    documentno = models.CharField(blank=True, null=True, max_length=1024)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    
    pri_tags = models.JSONField(blank=False, null=False, default=list) # models.ForeignKey(PrimaryTags, on_delete=models.CASCADE, blank=False, null=False)
    sec_tags = models.JSONField(blank=False, null=False, default=list) # models.ForeignKey(SecondaryTags, on_delete=models.CASCADE, blank=False, null=False)
    
    def __str__(self):
        return (
            "<[ Article ]>" + " || "
            f"TITLE - {self.title}" + " || "
            f"DATE - {self.date}" + " || "
            f"FROM - {self.source.name}" + " || "
            f"INDEX_NO - {self.indexno}" + " || "
            f"DOCUMENT_NO - {self.documentno}" + " || "
            f"CATEGORY - {self.category.name}" + " || "
            f"REGION - {self.region.name}" + " || "
            f"PRI_TAGs - {self.pri_tags}" + " || "
            f"SEC_TAGs - {self.sec_tags}"
        )
    
    @property
    def pri_tags_str(self):
        return '、'.join( tag for tag in self.pri_tags )
    @property
    def sec_tags_str(self):
        return '、'.join( tag for tag in self.sec_tags )














































