# Trivia: I had to use get_user_model, otherwise i encounter : "AttributeError: 'NoneType' object has no attribute '_meta' error"
from django.contrib.auth import get_user_model 
User = get_user_model() 

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, status, exceptions
from .models import Collection


class CreateCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

class CollectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['collection_title','collection_key']

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'
    