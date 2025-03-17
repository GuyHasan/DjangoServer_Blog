from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user= User.objects.create_user(**validated_data)
        user.groups.add(2)
        return user
    
    def __str__(self):
        return f'{self.username}'