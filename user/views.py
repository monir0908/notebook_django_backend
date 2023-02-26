from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status

from .serializers import (
    CustomTokenObtainPairSerializer,
    UserSignUpSerializer,
)
# USER LOGIN
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# USER REGISTRATION
class SignUpView(APIView):
    
    def post(self,request):
        request.data['is_active'] = True

        serializer = UserSignUpSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
            ## sending email to user
            # user = User(
            #     email = serializer.data['email'],
            #     first_name = serializer.data['first_name'],
            #     last_name = serializer.data['last_name']                
            # )
            # send_email(user)

            return JsonResponse(status=status.HTTP_201_CREATED, data={    
                "success": True,
                "state": "success",
                "message": "Registration successful!",
            })