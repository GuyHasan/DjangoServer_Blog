from rest_framework.viewsets import ModelViewSet
from .models import Article
from .serializers import ArticleSerializer
from utils.permissions import  IsAdminUser, IsAdminOrEditorUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from utils.filter_classes import ArticleFilter



class ArticlePagination(PageNumberPagination):
    page_size =3
    page_size_query_param = 'page_size'  
    max_page_size = 36  



class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ArticleFilter
    filterset_fields = ['author', 'tags']
    search_fields = ['title', 'content', 'tags__name', 'author__username']
    pagination_class = ArticlePagination
    
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
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().order_by('-publish_date'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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

