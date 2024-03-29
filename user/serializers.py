# Trivia: I had to use get_user_model, otherwise i encounter : "AttributeError: 'NoneType' object has no attribute '_meta' error"
from django.contrib.auth import get_user_model 
User = get_user_model() 
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer, 
    TokenObtainSerializer
)

from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, status, exceptions
from base.helpers import generate_user_code
from django.conf import settings
from django.templatetags.static import static

from pathlib import Path
import os
from django.conf import settings
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer, TokenObtainSerializer):

    def get_profile_pic_url(self, user):
        if os.path.isdir(os.path.join(settings.MEDIA_ROOT, 'profile_pics')) and user.profile_pic:
            return self.context['request'].build_absolute_uri(self.user.profile_pic_thumbnail.url)
        else:
            # Return a default profile picture URL or a placeholder image URL
            return self.context['request'].build_absolute_uri(static('default_images/avatar.png'))
            return "https://trello-members.s3.amazonaws.com/63cf43cec74fb1aa9b684de0/783f74cf34e7bdf05e5e6d61f0887fb7/30.png"
    
  
    # Overiding validate function in the TokenObtainSerializer  
    def validate(self, attrs):
        
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
            
        except KeyError:
            raise KeyError('One or more key is missing')

        # print(f"\nthis is the user of authenticate_kwargs {authenticate_kwargs['email']}\n")
       
        
        '''
        Checking if the user exists by getting the email(username field) from authentication_kwargs.
        If the user exists we check if the user account is active.
        If the user account is not active we raise the exception and pass the message. 
        Thus stopping the user from getting authenticated altogether. 
        
        And if the user does not exist at all we raise an exception with a different error message.
        Thus stopping the execution righ there.  
        '''
        try:
            user = User.objects.get(email=authenticate_kwargs['email'])
            if not user.is_active:
             self.error_messages['no_active_account']=_(
                 'You have been restricted by admin. Your account is set to inactive.'
            )
             raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
                )
            # if not user.is_staff:
            #     self.error_messages['not_a_staff']=_(
            #     'You are not a staff. Therefore, you are not allowed to login.'
            # )
            #     raise exceptions.AuthenticationFailed(
            #      self.error_messages['not_a_staff'],
            #      'not_a_staff',
            # )
        except User.DoesNotExist:
            self.error_messages['no_active_account'] =_(
              'Account does not exist')
            raise exceptions.AuthenticationFailed(
              self.error_messages['no_active_account'],
              'no_active_account',
            )
          
        '''
        We come here if everything above goes well.
        Here we authenticate the user.
        The authenticate function return None if the credentials do not match 
        or the user account is inactive. However here we can safely raise the exception
        that the credentials did not match as we do all the checks above this point.
        '''
        
        self.user = authenticate(**authenticate_kwargs)
        if self.user is None:
            self.error_messages['username_or_pass_incorrect'] = _(
                'Username or password is incorrect.')
            raise exceptions.AuthenticationFailed(
                self.error_messages['username_or_pass_incorrect'],
                'username_or_pass_incorrect',
            )
        # return super().validate(attrs)
    
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Adding extra responses here
        data['id'] = self.user.id
        data['full_name'] = self.user.get_full_name()
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['email'] = self.user.email
        data['user_code'] = self.user.user_code
        data['is_active'] = self.user.is_active
        data['is_staff'] = self.user.is_staff
        data['is_superuser'] = self.user.is_superuser
        data['profile_pic'] = self.get_profile_pic_url(self.user)

        # # Add profile_pic field to the response data
        # if self.user.profile_pic:
        #     profile_pic_url = self.context['request'].build_absolute_uri(self.user.profile_pic.url)
        #     data['profile_pic'] = profile_pic_url
        # data['groups'] = self.user.groups.values_list('name', flat=True) <--Encounter Error:  TypeError: Object of type QuerySet is not JSON serializable
        return data

class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'mobile',
            'password',
        ]
    def create(self, validated_data):
        
        user = self.Meta.model(**validated_data)

        # Getting password from dictionary for hashing
        password = validated_data.pop('password')
        

        user.set_password(password)
        user.is_active = True
        user.user_code = generate_user_code()    
        
        # Saving user model
        user.save()       
        return user


class ProfilePicUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('profile_pic',)
        read_only_fields = ('profile_pic_thumbnail',)

    def update(self, instance, validated_data):
        profile_pic = validated_data.get('profile_pic')
        if profile_pic:
            instance.profile_pic = profile_pic
            instance.save()
        return instance
    

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)

    def validate_first_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("First name must be at least 2 characters long.")
        return value