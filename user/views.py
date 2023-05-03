from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError, APIException
from django.http import Http404
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import get_user_model 
User = get_user_model() 
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserSignUpSerializer,
    ProfilePicUpdateSerializer,
    ProfileUpdateSerializer,
)
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
import os
from base.utils import send_email
from collection.serializers import CreateCollectionSerializer

# USER VIEWS
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class SignUpView(APIView):
    def post(self,request):
        request.data['is_active'] = True
        

        serializer = UserSignUpSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            
            try:
                # creating a sample collection as default
                request.data['collection_title'] = "Sample"
                request.data['collection_creator'] = user.id        
                

                serializer = CreateCollectionSerializer(data = request.data)

                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                
                # sending an welcome email
                send_email(user)  # did not use post_save as unable to catch exceptions from post_save
                """
                SMTP does not perform email address validation during email sending. It simply sends 
                the email to the specified address without verifying if the email address actually exists or not. 
                The email server at the recipient's end may later reject the email if the address does not exist, 
                or if it is invalid for some other reason. Therefore, SMTP does not throw an 
                exception even if the email address is wrong (e.g. monir@fakefake.com)
                """
            except Exception as e:
                return JsonResponse(status=status.HTTP_200_OK, data={    
                    "state": "success",
                    "message": "Sign up successful! However, failed to send welcome email or create sample collection; Error: {}".format(str(e))
                })
            else:
                return JsonResponse(status=status.HTTP_200_OK, data={    
                    "state": "success",
                    "message": "Sign up successful! Check your email for further instructions.",
                })

        return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={
            "success": False,
            "state": "failure",
            "message": "Failed to create user account. Please try again later."
        })

class ProfilePicUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = ProfilePicUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():                
            # Save new profile pic
            image_data = request.FILES.get('profile_pic')
            if image_data:
                filename = f"{user.id}_{user.first_name}.{image_data.name.split('.')[-1]}"
                filepath = default_storage.save(os.path.join('profile_pics', filename), ContentFile(image_data.read()))
                print("==============3===============")
                print(f"NEW IMAGE SAVBING PATH: {filepath}")
                print("=============================")
                user.profile_pic = filepath
            user.save()
            # Get full URL for profile pic
            print(user.profile_pic.url)
            profile_pic_url = request.build_absolute_uri(user.profile_pic_thumbnail.url)
            
            return JsonResponse(status=status.HTTP_200_OK, data={    
                "state": "success",
                "message": "profile pic uploaded..",
                "profile_pic": profile_pic_url,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class ProfileUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def put(self, request, *args, **kwargs):       

        try:
            instance = self.get_object()
        except Http404:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={
                "state": "warning",
                "message": "Invalid user ID."
            })
        
        try:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except Exception as e:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={
                "state": "error",
                "message": str(e)
            })            

        # return updated fields in response
        return JsonResponse(status=status.HTTP_200_OK, data={
            "state": "success",
            "message": "Profile updated..",
            "first_name": serializer.data.get('first_name', instance.first_name),
            "last_name": serializer.data.get('last_name', instance.last_name)
        })  

class PasswordChangeAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):   # The Django UpdateAPIView maps to the HTTP PUT method by default.
        user = self.get_object()
        old_password = request.data.get('old_password', None)
        new_password = request.data.get('new_password', None)

        if not old_password or not new_password:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={    
                "state": "warning",
                "message": "Both old password and new password fields are required.",
            })

        if not check_password(old_password, user.password):
            return JsonResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={   
                "state": "warning",
                "message": "Invalid old password.",
            })

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={    
                "state": "warning",
                "message": f"Passwords validation failed. {e.messages}",
            })            

        user.set_password(new_password)
        user.save()
        return JsonResponse(status=status.HTTP_200_OK, data={    
            "state": "success",
            "message": "Password successfully updated...",
        })