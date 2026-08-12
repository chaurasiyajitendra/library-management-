from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/",views.register,name="register"),
    path("login/",views.login,name="login"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("search-books/",views.search_books,name="search_books"),
    path("rent/<int:id>/", views.rent_book, name="rent_book"),
    path("return/<int:id>/",views.return_book,name="return_book"),
]
