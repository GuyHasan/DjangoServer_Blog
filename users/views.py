from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from utils.permissions import IsAdminUser



# Create your views here.
class UserViewSet(ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def list(self, request):
        """Returns a list of users (required for appearing in API root)."""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = RefreshToken.for_user(user)
            return Response({
                "user": serializer.data,
                "refresh": str(token),  # Refresh token
                "access": str(token.access_token),  # Access token
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            token = RefreshToken.for_user(user)
            return Response({'message': 'Login success',
                            'refresh': str(token),
                            'access': str(token.access_token)
                            }, status=status.HTTP_200_OK)
        return Response({'message': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)
    


    