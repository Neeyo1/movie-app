from django.urls import path

from . import views

urlpatterns = [
    #index
    path("", views.index, name="index"),
    #login
    path("login/", views.login_to_page, name="login_to_page"),
    #logout
    path("logout/", views.logout_from_page, name="logout_from_page"),
    #register
    path("register/", views.register_to_page, name="register_to_page"),
    #movie
    #path("movie/<int:movie_id>/", views.movie_detail, name="movie_detail"),
    #path("movie/create/", views.movie_create, name="movie_create"),
    #path("movie/edit/<int:movie_id>", views.movie_edit, name="movie_edit"),
    #path("movie/delete/<int:movie_id>", views.movie_delete, name="movie_delete"),
    #path("movie/public-private/<int:movie_id>", views.movie_public_private, name="movie_public_private"),
]