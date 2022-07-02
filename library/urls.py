from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("donate", views.donate, name="donate"),
    path("search", views.search, name="search"),
    path("profile", views.profile, name="profile"),
    path("editbook/<int:id>", views.edit, name="edit"),   
    #APIs:
    path("book/<int:id>",views.book,name="book"), #show info of a book
    path("deletebook",views.delete,name="delete"), #delete a book
    
]