import uuid
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.account import serializers
from apps.account.models import CustomUser
from apps.account.send_mail import send_password

User = get_user_model()


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()


        return Response(serializer.data, status=201)


class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)



class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer




class ForgotPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)
    @staticmethod
    def post(request):
        email = request.data.get('email')
        if not email:
            return Response({'msg': 'Необходимо предоставить адрес электронной почты'}, status=400)

        try:
            assert '@' in email
            user = CustomUser.objects.get(email=email)
            if user.forgot_password_reset != '':
                return Response({'msg': 'проверьте почту!'}, status=201)
            user.forgot_password_reset = uuid.uuid4()
            user.save()
            send_password(user.email, user.forgot_password_reset)
            return Response({'msg': 'код для сброса отправлен на почту!'}, status=200)
        except:
            return Response({'msg': 'Такого аккаунта не существует'}, status=404)

    @staticmethod
    def put(request):
        try:
            serializer = serializers.ForgotPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        except User.DoesNotExist:
            return Response({'неверный код'}, status=400)
        return Response({'Поздравляю вы успешно поменяли свой пароль'}, status=201)
