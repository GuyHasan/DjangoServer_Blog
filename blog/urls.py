from rest_framework.routers import DefaultRouter
from django.urls import path, include
from users.views import UserViewSet
from articles.views import ArticleViewSet
from comments.views import CommentViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('api/', include(router.urls)), 
]
