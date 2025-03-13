from rest_framework.viewsets import ModelViewSet
from .models import Article
from .serializers import ArticleSerializer
from utils.permissions import IsEditorUser, IsAdminUser, IsRegularUser

# Create your views here.
class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = []
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsEditorUser]
        if self.action == 'destroy':
            self.permission_classes = [IsAdminUser]
        if self.action == 'partial_update':
            self.permission_classes = [IsAdminUser, IsEditorUser]
        if self.action == 'update':
            self.permission_classes = [IsAdminUser, IsEditorUser]
        return super().get_permissions()