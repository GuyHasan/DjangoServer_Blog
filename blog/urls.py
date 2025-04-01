from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CustomApiRootView
from users.views import UserViewSet
from articles.views import ArticleViewSet
from comments.views import CommentViewSet
from django.contrib import admin

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'comments', CommentViewSet, basename='comment')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', CustomApiRootView.as_view(), name='api-root'),
    path('api/', include(router.urls)), 
    path('api/article/<int:article_id>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comments-for-article'),
    path('api/users/', UserViewSet.as_view({'get': 'list'}), name='users'),
    path('api/login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('api/register/', UserViewSet.as_view({'post': 'register'}), name='register'),
    ]
