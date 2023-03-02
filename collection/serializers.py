# Trivia: I had to use get_user_model, otherwise i encounter : "AttributeError: 'NoneType' object has no attribute '_meta' error"
from django.contrib.auth import get_user_model 
User = get_user_model() 

from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, status, exceptions
from .models import Collection
from document.serializers import ( 
    DocumentSerializer, 
    CreateDocumentSerializer, 
    DocumentTinySerializer,
)

from document.models import Document
from base.enums import DocumentStatus

class CreateCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

class CollectionSerializer(serializers.ModelSerializer):

    # if children to be picked up straight
    # documents = DocumentTinySerializer(many=True, read_only=True)


    collection_creator_full_name = serializers.CharField(source='collection_creator.get_full_name', read_only=True)
    documents = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = [
            'id',
            'collection_title',
            'collection_key',
            'collection_creator_full_name',
            'documents'
        ]
    
    # if children to be picked up under condition
    def get_documents(self, obj):
        queryset = Document.objects.filter(~Q(doc_status = DocumentStatus.DELETED.value))
        return  DocumentTinySerializer(queryset, many=True).data

class CollectionTinySerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = [
            'id',
            'collection_title',
            'collection_key',
        ]
    