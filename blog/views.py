from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decouple import config

api_url= config("API_URL", default="http://localhost:8000/")

class CustomApiRootView(APIView):
    permission_classes = []
    def get(self, request, *args, **kwargs):
        # Customize the response here. For example, add custom links or info.
        return Response(
            {
            'message': 'Welcome to the API!',
            'endpoints': {
                'articles': {
                    'list': f'{api_url}api/articles/',
                    'detail': f'{api_url}api/articles/<int:id>/',
                    'comments': f'{api_url}api/article/<int:article_id>/comments/',
                },
                'comments': {
                    'list': f'{api_url}api/comments/',
                    'detail': f'{api_url}api/comments/<int:id>/',
                    'post': f'{api_url}api/article/<int:article_id>/comments/',
                },
                'users':{
                    'list': f'{api_url}api/users/',
                    'login': f'{api_url}api/login/',
                    'register': f'{api_url}api/register/',
                }
                ,
            }
            },
            status=status.HTTP_200_OK
        )