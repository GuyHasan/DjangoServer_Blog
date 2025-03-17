from rest_framework.viewsets import ModelViewSet
from .models import Article
from .serializers import ArticleSerializer
from utils.permissions import  IsAdminUser, IsAdminOrEditorUser

# Create your views here.
class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = []
    
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
