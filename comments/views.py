from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Comment
from articles.models import Article
from .serializers import CommentSerializer
from utils.permissions import AnyUser, IsOwner, IsAdminUser
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import status
from rest_framework.exceptions import NotFound



# Create your views here.

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = []

    def get_queryset(self):
        article_id = self.kwargs.get('article_id')
        if article_id:
            if not Article.objects.filter(id=article_id).exists():
                raise NotFound({"detail": "Article not found."})  
            return Comment.objects.filter(article=article_id)
        return Comment.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AnyUser]
        if self.action == 'destroy':
            self.permission_classes = [IsAdminUser]
        if self.action == 'partial_update':
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        try:
            article = Article.objects.get(id=self.kwargs['article_id'])
        except Article.DoesNotExist:
            return NotFound({"detail": "Article not found."})
        
        user = self.request.user        
        data = request.data.copy()  
        data['article'] = article.id  
        data['author'] = user.id  

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Comment created successfully."}, status=status.HTTP_201_CREATED)


    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        comments = res.data
        comments_dict = {comment["id"]: comment for comment in comments}
        root_comments = []
        for comment in comments:
            parent_id = comment['reply_to']
            if parent_id is None:
                root_comments.append(comment)
            else:
                parent = comments_dict.get(parent_id)
                if parent:
                    if "replies" not in parent:
                        parent["replies"] = []
                    parent["replies"].append(comment)
        res.data = root_comments
        return res
    

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()        
        data = request.data
        if 'content' in data:
            instance.content = data['content']
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        
        return Response({"detail": "Content field is required."}, status=400)


    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT",detail="Full update is not allowed. Use PATCH instead")