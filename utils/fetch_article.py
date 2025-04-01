from rest_framework import serializers
from articles.models import Article

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