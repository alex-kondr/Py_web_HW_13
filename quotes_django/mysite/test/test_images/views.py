import os

from django.shortcuts import redirect, render
from django.conf import settings

from .forms import PictureForm
from .models import Picture
# Create your views here.


def index(request):
    return render(request, 
                  "test_images/index.html",
                  context={"title": "Images list"})
    
def upload(request):
    
    form = PictureForm(instance=Picture())
    
    if request.method == "POST":
        form = PictureForm(request.POST, request.FILES, instance=Picture())
        
        if form.is_valid():
            form.save()
            
            # return redirect(to="test_images:index")
            
    return render(request,
                  "test_images/upload.html",
                  context={"title": "Images list",
                           "form": form})
    

def pictures(request):
    pictures = Picture.objects.all()
    return render(request,
                  "test_images/pictures.html",
                  context={"title": "Images list",
                           "pictures": pictures})
    
    
def remove_picture(request, pic_id):    
    pic = Picture.objects.filter(pk=pic_id)
    
    try:
        os.unlink(os.path.join(settings.MEDIA_ROOT, str(pic.first().path)))
    except OSError as e:
        print(e)
        
    pic.delete()
    return redirect(to="test_images:pictures")


def edit_picture(request, pic_id):
    
    if request.method == "POST":
        description = request.POST["description"]
        Picture.objects.filter(pk=pic_id).update(description=description)
        return redirect(to="test_images:pictures")
    
    picture = Picture.objects.filter(pk=pic_id).first()
    context={"title": "Images list","picture": picture}
    return render(request, 
                  "test_images/edit.html", 
                  context=context)