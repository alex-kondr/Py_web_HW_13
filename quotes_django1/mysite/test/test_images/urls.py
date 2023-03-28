from django.urls import path

from . import views


app_name = "test_images"

urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.upload, name="upload"),
    path("pictures/", views.pictures, name="pictures"),
    path("pictures/remove/<int:pic_id>", views.remove_picture, name="remove"),
    path("pictures/edit/<int:pic_id>", views.edit_picture, name="edit"),
]