# Trivia: I had to use get_user_model, otherwise i encounter : "AttributeError: 'NoneType' object has no attribute '_meta' error"
from django.contrib.auth import get_user_model 
User = get_user_model() 

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, status, exceptions
from .models import Collection
from document.serializers import DocumentSerializer, CreateDocumentSerializer, DocumentTinySerializer


class CreateCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

class CollectionSerializer(serializers.ModelSerializer):
    documents = DocumentTinySerializer(many=True, read_only=True)
    collection_creator_full_name = serializers.CharField(source='collection_creator.get_full_name', read_only=True)

    class Meta:
        model = Collection
        fields = [
            'id',
            'collection_title',
            'collection_key',
            'collection_creator_full_name',
            'documents'
        ]
    