from rest_framework.viewsets import ModelViewSet
from .models import Article
from .serializers import ArticleSerializer
from utils.permissions import  IsAdminUser, IsAdminOrEditorUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

# Create your views here.
class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'content', 'tags', 'author']
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAdminOrEditorUser]
        if self.action == 'destroy':
            self.permission_classes = [IsAdminUser]
        if self.action == 'partial_update':
            self.permission_classes = [IsAdminOrEditorUser]
        if self.action == 'update':
            self.permission_classes = [IsAdminOrEditorUser]
        return super().get_permissions()
    
    def get_queryset(self):
        queryset =  super().get_queryset()
        title = self.request.query_params.get('title', None)
        content = self.request.query_params.get('content', None)
        tags = self.request.query_params.get('tags', None)
        author = self.request.query_params.get('author', None)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if content:
            queryset = queryset.filter(content__icontains=content)
        if tags:
            queryset = queryset.filter(tags__icontains=tags)
        if author:
            queryset = queryset.filter(author__username=author)
        return queryset
    

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            response.data = {'message': 'Article deleted successfully'}
        return response
    

    def update(self, request, *args, **kwargs):
        obj = self.get_object()  # Ensure we're working with a specific object
        self.check_object_permissions(request, obj)  # Manually call object permission check
        return super().update(request, *args, **kwargs)
    

    def partial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_object_permissions(request, obj)
        return super().partial_update(request, *args, **kwargs)

