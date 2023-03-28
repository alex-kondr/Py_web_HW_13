from django.urls import path

from . import views


app_name = "my_quotes"

urlpatterns = [
    path("", views.index, name="index"),
    path("page/<int:page>", views.index, name="next_page"),
    path("author/<author_name>", views.get_author, name="author"),
    path("tag/<tag>", views.get_quotes_of_tag, name="tag"),
    path("delete_quote/<int:quote_id>/<int:page>", views.delete_quote, name="delete_quote"),
    path("add_quote/<int:quote_id>", views.edit_quote, name="edit_quote"),
    path("add_quote/", views.add_quote, name="add_quote"),
    path("add_author/", views.add_author, name="add_author"),
]
