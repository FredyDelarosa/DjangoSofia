"""
URL configuration for sofia_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from .views.home import HomeView
from django.contrib.auth import views as auth_views
from .views.auth_views import register
from .views.article_views import (
    ArticleListView, ArticleDetailView, ArticleCreateView,
    ArticleUpdateView, ArticleDeleteView
)
from .views.movie_views import (
    MovieListView, MovieDetailView, MovieCreateView, MovieUpdateView, MovieDeleteView
)
from .views.comment_views import CommentListView, CommentCreateView, CommentDeleteView, CommentUpdateView

from .views.award_views import AwardListView, AwardDetailView, AwardCreateView, AwardUpdateView, AwardDeleteView

from sofia_blog.views.websocket_views import websocket_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('movies/', MovieListView.as_view(), name='movie_list'),
    path('movies/create/', MovieCreateView.as_view(), name='movie_create'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('movies/<int:pk>/edit/', MovieUpdateView.as_view(), name='movie_edit'),
    path('movies/<int:pk>/delete/', MovieDeleteView.as_view(), name='movie_delete'),
    path('movies/<int:movie_id>/comments/', CommentListView.as_view(), name='comment_list'),
    path('movies/<int:movie_id>/comment/create/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_edit'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('awards/', AwardListView.as_view(), name='award_list'),
    path('awards/create/', AwardCreateView.as_view(), name='award_create'),
    path('awards/<int:pk>/', AwardDetailView.as_view(), name='award_detail'),
    path('awards/<int:pk>/edit/', AwardUpdateView.as_view(), name='award_edit'),
    path('awards/<int:pk>/delete/', AwardDeleteView.as_view(), name='award_delete'),
    #path('socket/', include('sofia_blog.routingsocket')),
    path("websocket-view/", websocket_view, name="websocket_view"),
]

