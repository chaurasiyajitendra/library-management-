from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="deshboard"),
    path("books/",views.books,name="director_books"),
    path("books/add/",views.add_book,name="add_book"),
    path("books/edit/<int:id>/",views.edit_book,name="edit_book"),
    path("books/delete/<int:id>/",views.delete_book,name="delete_book"),
    path("rentals/",views.rentals,name="director_rentals"),
    path("users/",views.users,name="director_users"),
    path("users/<int:id>/",views.user_detail,name="user_detail"),
    path("users/delete/<int:id>/",views.delete_user,name="delete_user"),
]