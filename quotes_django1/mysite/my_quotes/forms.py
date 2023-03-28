from django.contrib.auth.models import User
from django.forms import ModelForm, CharField, TextInput, Textarea, DateField, DateInput

from .models import Quote, Author


class AuthorForm(ModelForm):
    
    fullname = CharField(max_length=200, widget=TextInput(attrs={"class": "form-control"}))
    born_date = DateField(widget=DateInput(attrs={"class": "form-control"}))
    born_location = CharField(max_length=200, widget=TextInput(attrs={"class": "form-control"}))
    description = CharField(widget=Textarea(attrs={"class": "form-control"}))
    
    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]


class QuoteForm(ModelForm):
    
    quote = CharField(widget=Textarea(attrs={"class": "form-control"}))
    tags = CharField(max_length=500, widget=TextInput(attrs={"class": "form-control"}))
    author = Author
    user = User
        
    class Meta:
        model = Quote
        fields = ["quote", "tags", "author", "user"]