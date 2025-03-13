from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from .serializers import CommentSerializer
from utils.parse_int import try_parse_int
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsRegularUser, IsAdminUser
from rest_framework.exceptions import MethodNotAllowed



# Create your views here.

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = []

    def get_queryset(self):
        article_id = self.request.query_params.get('article_id')
        if article_id:
            return Comment.objects.filter(article=article_id)
        return Comment.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'destroy':
            self.permission_classes = [IsAdminUser, IsRegularUser]
        if self.action == 'partial_update':
            self.permission_classes = [IsAdminUser, IsRegularUser]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        data = request.data
        reply_to = data.get('reply_to')
        article = try_parse_int(data.get('article'))
        if reply_to:
            repliedComment = Comment.objects.get(id=reply_to)
            if (repliedComment and repliedComment.article.id != article):
                return Response(
                    {'error': 'Comment must be in the same article as the replied comment'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)


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