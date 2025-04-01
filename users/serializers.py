from rest_framework.serializers import ModelSerializer, Serializer, CharField
from django.contrib.auth.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    def __str__(self):
        return f'{self.username}'
    
    def create(self, validated_data):
        validated_data.pop('groups', None)
        validated_data.pop('user_permissions', None)
        user= User.objects.create_user(**validated_data)
        return user
    
    def get_fields(self):
        fields = super().get_fields()
        view = self.context.get('view')  
        if view and hasattr(view, 'action'): 
            if view.action == 'login':
                excluded_fields = ['id', 'last_login', 'is_staff', 'is_superuser',
                                'groups', 'user_permissions', 'date_joined', 'is_active', 'email', 'first_name', 'last_name']
            elif view.action == 'register':
                excluded_fields = ['id', 'last_login', 'is_staff', 'is_superuser',
                                'groups', 'user_permissions', 'date_joined', 'is_active']
            else:
                excluded_fields = []
        else:
            excluded_fields = []  

        for field in excluded_fields:
            fields.pop(field, None) 

        return fields



class LoginSerializer(Serializer):
    username = CharField()
    password = CharField(write_only=True)