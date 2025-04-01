from django_filters import rest_framework as filters
from articles.models import Article

class ArticleFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    content = filters.CharFilter(lookup_expr='icontains')
    author = filters.CharFilter(field_name='author__username', lookup_expr='icontains')  # Assuming 'author' is a ForeignKey
    tags = filters.CharFilter(field_name='tags__name', lookup_expr='icontains')  # Assuming tags is ManyToMany with 'name' field

    class Meta:
        model = Article
        fields = ['title', 'content', 'author', 'tags']  # You can also specify more fields here
