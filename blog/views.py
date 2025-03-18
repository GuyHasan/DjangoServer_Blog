from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CustomApiRootView(APIView):
    permission_classes = []
    def get(self, request, *args, **kwargs):
        # Customize the response here. For example, add custom links or info.
        return Response(
            {
                'message': 'Welcome to the API!',
                'endpoints': {
                    'articles': '/api/articles/',
                    'comments': '/api/comments/',
                    'users': '/api/users/',
                }
            },
            status=status.HTTP_200_OK
        )