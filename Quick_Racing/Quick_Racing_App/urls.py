from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('loginreg', views.loginreg),
    path('register', views.register),
    path('logout', views.logout),
    path('login', views.login),
    path('news', views.news),
    path('forum', views.forum),
    path('shop', views.shop),
    path('createnews', views.newarticlepage),
    path('createarticle', views.newarticle),
    path('article/<article_id>/like_article', views.likearticle),
    path('createpost', views.newpostpage),
    path('create-post', views.addpost),
    path('post/<post_id>', views.post),
    path('editpost/<post_id>', views.editpost),
    path('post/<int:post_id>/update', views.update),
    path('post/<int:post_id>/delete', views.delete),
    path('purchase', views.purchase),
]
