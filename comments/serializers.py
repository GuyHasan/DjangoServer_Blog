from rest_framework import serializers
from rest_framework.fields import HiddenField, CurrentUserDefault
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    author = HiddenField(default= CurrentUserDefault())
    class Meta:
        model = Comment
        fields = '__all__'

    def update(self, instance, validated_data):
        # Ensure only 'content' can be updated during a partial update
        content = validated_data.get('content', None)
        if content:
            instance.content = content  # Update content field
        instance.save()
        return instance