# Trivia: I had to use get_user_model, otherwise i encounter : "AttributeError: 'NoneType' object has no attribute '_meta' error"
from django.contrib.auth import get_user_model 
User = get_user_model() 

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, status, exceptions
from .models import Document

class CreateDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):

    collection_title = serializers.CharField(source='collection.collection_title', read_only=True)
    collection_key = serializers.CharField(source='collection.collection_key', read_only=True)
    doc_creator_full_name = serializers.CharField(source='doc_creator.get_full_name', read_only=True)

    class Meta:
        model = Document
        fields = '__all__'
        extra_fields = [
            'collection_title',
            'collection_key',
            'doc_creator_full_name',
        ]
    