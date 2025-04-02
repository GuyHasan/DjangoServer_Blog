from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Comment
from articles.models import Article
from .serializers import CommentSerializer
from utils.permissions import AnyUser, IsOwner, IsAdminUser
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.utils.functional import SimpleLazyObject
from rest_framework.pagination import PageNumberPagination



class CommentPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 1000

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = []
    pagination_class = CommentPagination

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
        if request.parser_context["kwargs"].get("article_id") is None:
            return Response(
                {"error": "Direct comment creation is not allowed. Use /api/articles/{article_id}/comments/ instead."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            article = Article.objects.get(id=self.kwargs['article_id'])
        except Article.DoesNotExist:
            return NotFound({"detail": "Article not found."})
        user = request.user
        if isinstance(user, SimpleLazyObject):
            user = user._wrapped  
        data = request.data.copy()
        data['author'] = user.id  

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(article=article, author=user)

        return Response({"detail": "Comment created successfully.", "comment": serializer.data}, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        comments = res.data.get('results', [])
        comments_dict = {comment["id"]: comment for comment in comments}
        root_comments = []
        for comment in comments:
            parent_id = comment.get('reply_to')
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

        # Check if there are any fields other than 'content'
        if set(data.keys()) - {'content'}:
            return Response({"detail": "Only 'content' field is allowed to be updated."}, status=400)

        if 'content' in data:
            instance.content = data['content']
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data , status=200)

        return Response({"detail": "Content field is required."}, status=400)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT",detail="Full update is not allowed. Use PATCH instead")

        
    


