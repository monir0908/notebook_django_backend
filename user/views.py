from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model 
User = get_user_model() 
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserSignUpSerializer,
    ProfilePicUpdateSerializer,
)
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os



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

class ProfilePicUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = ProfilePicUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            # Delete old profile pic if it exists
            if user.profile_pic:
                default_storage.delete(user.profile_pic.path)
            # Save new profile pic
            image_data = request.FILES.get('profile_pic')
            if image_data:
                filename = f"{user.id}_profile_pic.{image_data.name.split('.')[-1]}"
                filepath = default_storage.save(os.path.join(settings.MEDIA_ROOT, filename), ContentFile(image_data.read()))
                user.profile_pic = filepath
            user.save()
            # Get full URL for profile pic
            profile_pic_url = request.build_absolute_uri(user.profile_pic.url)
            
            return JsonResponse(status=status.HTTP_200_OK, data={    
                "state": "success",
                "message": "profile pic uploaded..",
                "profile_pic": profile_pic_url,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)