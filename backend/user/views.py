# users/views.py
from django.contrib.auth import get_user_model, authenticate
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, MagicLinkSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class MagicLinkLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = MagicLinkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()
        if user:
            magic_link_token = get_random_string(32)
            # Save magic_link_token to user profile (you'll need to add a field for this)
            user.magic_link_token = magic_link_token
            user.save()

            magic_link_url = f"{settings.FRONTEND_URL}/magic-link-login?token={magic_link_token}"
            send_mail(
                'Your Magic Link for CSIS Asset Management System',
                f'Click the link to login: {magic_link_url}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            return Response({'message': 'Magic link sent'}, status=status.HTTP_200_OK)
        return Response({'error': 'Email not found'}, status=status.HTTP_400_BAD_REQUEST)

class MagicLinkVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        user = User.objects.filter(magic_link_token=token).first()
        if user:
            # Clear the token once used
            user.magic_link_token = ''
            user.save()
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid or expired magic link'}, status=status.HTTP_400_BAD_REQUEST)
