from django.db import models
from django.contrib.auth.models import User
from django_mysql.models import ListCharField


class Author(models.Model):
    
    fullname = models.CharField(max_length=255)
    born_date = models.DateTimeField()
    born_location = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.fullname
    

class Quote(models.Model):
    
    tags = ListCharField(base_field=models.CharField(max_length=50), max_length=500)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True)
