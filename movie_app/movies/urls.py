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
    path("movie/", views.movie, name="movie"),
    path("movie/<int:movie_id>/", views.movie_detail, name="movie_detail"),
    path("movie/create/", views.movie_create, name="movie_create"),
    path("movie/edit/<int:movie_id>", views.movie_edit, name="movie_edit"),
    path("movie/delete/<int:movie_id>", views.movie_delete, name="movie_delete"),
    path("movie/public-private/<int:movie_id>", views.movie_public_private, name="movie_public_private"),
    #genre
    path("genre/", views.genre, name="genre"),
    path("genre/<int:genre_id>/", views.genre_detail, name="genre_detail"),
    path("genre/create/", views.genre_create, name="genre_create"),
    path("genre/edit/<int:genre_id>", views.genre_edit, name="genre_edit"),
    path("genre/delete/<int:genre_id>", views.genre_delete, name="genre_delete"),
    #tag
    path("tag/", views.tag, name="tag"),
    path("tag/<int:tag_id>/", views.tag_detail, name="tag_detail"),
    path("tag/create/", views.tag_create, name="tag_create"),
    path("tag/edit/<int:tag_id>", views.tag_edit, name="tag_edit"),
    path("tag/delete/<int:tag_id>", views.tag_delete, name="tag_delete"),
]