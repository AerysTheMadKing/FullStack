import uuid
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from account import serializers
from account.models import CustomUser
from account.send_mail import send_confirmation_email
User = get_user_model()


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            try:
                send_confirmation_email(user.email, user.activation_code)
            except:
                return Response({'msg': 'Registered, but troubles with email!', 'data': serializer.data}, status=201)


        return Response(serializer.data, status=201)



class ActivationView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg': 'Successfully activated!'}, status=200)
        except User.DoesNotExist:
            return Response({'msg': 'link expired or invalid!'}, status=404)




class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)



class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


