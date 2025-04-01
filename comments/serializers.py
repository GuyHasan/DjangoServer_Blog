from rest_framework import serializers
from rest_framework.fields import HiddenField, CurrentUserDefault
from .models import Comment
from utils.fetch_article import ArticleFromURL


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())
    article = serializers.PrimaryKeyRelatedField(read_only=True, default=ArticleFromURL())
    reply_to = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def get_fields(self):
        """Dynamically filter reply_to queryset to only show comments from the same article."""
        fields = super().get_fields()
        article_id = self.context.get('view', {}).kwargs.get('article_id')
        if article_id:
            try:
                article_id = int(article_id)  
                fields['reply_to'].queryset = Comment.objects.filter(article_id=article_id)
            except ValueError:
                pass  
        return fields
    
            

    def validate(self, data):
        """
        Custom validation to check if parent_comment belongs to the same article.
        """
        article_id = data.get('article').id
        reply_comment = data.get('reply_to')  
        if reply_comment:
            reply_comment_id = reply_comment.id
            reply_comment_article = Comment.objects.filter(id=reply_comment_id).values_list('article', flat=True).first()
            print("Article ID:", article_id, "Reply Comment ID:", reply_comment_id, "Reply Comment Article:", reply_comment_article)
            if reply_comment_article != article_id:
                raise serializers.ValidationError("You can only reply to comments from the same article.")

        return data
    
    


class ArticleFromURL:
    """Fetch article from URL, but don't overwrite if already provided."""
    requires_context = True

    def __call__(self, serializer_field):
        view = serializer_field.context.get('view', None)
        if view and hasattr(view, 'kwargs'):
            article_id = view.kwargs.get('article_id')
            if article_id:
                return Article.objects.get(id=article_id)
        raise serializers.ValidationError("Article ID is required in the URL.")
