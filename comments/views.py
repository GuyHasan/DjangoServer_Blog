from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from .serializers import CommentSerializer
from utils.parse_int import try_parse_int




# Create your views here.

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

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