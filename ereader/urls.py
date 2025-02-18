from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.upload_epub, name="upload_epub"),
    path("reader/<int:book_id>/<int:chunk_id>/", views.reader, name="reader"),
]