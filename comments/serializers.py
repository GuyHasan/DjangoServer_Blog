from rest_framework import serializers
from rest_framework.fields import HiddenField, CurrentUserDefault
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    author = HiddenField(default= CurrentUserDefault())
    class Meta:
        model = Comment
        fields = '__all__'
