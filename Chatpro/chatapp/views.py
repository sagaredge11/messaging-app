
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Message,UserProfile
from .serializers import MessageSerializer,UserSerializer
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import authenticate,login
from rest_framework.authtoken.models import Token
from rest_framework import status
# Create your views here.

class IndexView(viewsets.ViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        if request.user.is_authenticated:
            return Response({'message': 'User is Authenticated'})
        else:
            return Response({'message': 'User is Not Authenticated'})

    def create(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            print(token.key)
            return Response({'token': token.key})
        else:
            return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class UserView(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MessageView(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

