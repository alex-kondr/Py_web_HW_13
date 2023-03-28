from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Author, Quote
from .forms import AuthorForm, QuoteForm


class TopTags:
    
    def __init__(self, size, top_tag):
        self.style = f"font-size: {size}px"
        self.top_tag = top_tag    
    
    
def get_top_tags(quotes):
    
    tags = {}
    top_tags = []
    
    for quote in quotes:
        for tag in quote.tags:
            if tags.get(tag):
                tags[tag] += 1
            else:
                tags.update({tag: 1})
                
    for i in range(10):        
        if not tags:
            break
        
        top_tag = max(tags, key=tags.get)
        top_tags.append(TopTags(40-i*4, top_tag))
        tags.pop(top_tag)
    
    return top_tags    


@login_required
def add_author(request):
    
    if request.method == "POST":
        form = AuthorForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect(to="my_quotes:index")
        
        render(request,
               "my_quotes/add_author.html",
               context={"form": form})
    
    return render(request,
                  "my_quotes/add_author.html",
                  context={"form": AuthorForm()})


@login_required
def add_quote(request):
    
    if request.method == "POST":
        form = QuoteForm(request.POST)
        
        if form.is_valid():
            form.save()            
            return redirect(to="my_quotes:index")        
        
        return render(request, 
                        "my_quotes/add_edit_quote.html",
                        context={"form": form})  
    
    return render(request,
                  "my_quotes/add_edit_quote.html",
                  context={"form": QuoteForm()})
    
   
def index(request, page:int=1):
    
    quotes = Quote.objects.all()    
    paginator = Paginator(quotes, per_page=9)
    page_object = paginator.get_page(page)
    
    top_tags = get_top_tags(quotes)
    
    context={        
        "page_object": page_object,
        "top_tags": top_tags
        }
    
    return render(request,
                  "my_quotes/index.html",
                  context=context)

  
def get_quotes_of_tag(request, tag:str):
    
    quotes = Quote.objects.filter(tags__iregex=tag)
    paginator = Paginator(quotes, per_page=100)
    page_object = paginator.get_page(1)
    
    return render(request,
                  "my_quotes/index.html",
                  context={"page_object": page_object})


def get_author(request, author_name:str):
    author = Author.objects.filter(fullname=author_name).first()
    return render(request,
                  "my_quotes/author.html",
                  context={"author": author})   


@login_required
def edit_quote(request, quote_id:int):
    
    quote = Quote.objects.get(pk=quote_id)
    quote.tags = ",".join(quote.tags)
    
    if request.method == "POST":
        form = QuoteForm(request.POST, instance=quote)
        
        if form.is_valid():
            form.save()
            return redirect(to="my_quotes:index")
        
        return render(request,
                      "my_quotes/add_edit_quote.html",
                      context={"form": form,
                               "quote_id": quote_id})
        
    form = QuoteForm(instance=quote) 
     
    return render(request,
                  "my_quotes/add_edit_quote.html",
                  context={"form": form,
                           "quote_id": quote_id})


@login_required
def delete_quote(request, quote_id:int, page:int=1):
    
    quote = Quote.objects.get(pk=quote_id)
    quote.delete()
    
    return index(request, page)