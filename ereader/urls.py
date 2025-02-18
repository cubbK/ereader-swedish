from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.upload_epub, name="upload_epub"),
    path("reader/<int:book_id>/<int:chunk_id>/", views.reader, name="reader"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="ereader/login.html"),
        name="login",
    ),
    path("register/", views.register, name="register"),
]
