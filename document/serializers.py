# Trivia: I had to use get_user_model, otherwise i encounter : "AttributeError: 'NoneType' object has no attribute '_meta' error"
from django.contrib.auth import get_user_model 
User = get_user_model() 

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, status, exceptions
from .models import Document, Attachment
import os
from urllib.parse import urlparse
class AttachmentSerializer(serializers.ModelSerializer):
    file_name = serializers.SerializerMethodField()
    file_extension = serializers.SerializerMethodField()
    
    class Meta:
        model = Attachment
        fields = ('id', 'document', 'file', 'uploaded_at', 'file_name', 'file_extension')
    
    def get_file_name(self, obj):
        return os.path.basename(urlparse(obj.file.name).path)

    def get_file_extension(self, obj):
        return os.path.splitext(obj.file.name)[1]
    

class CreateDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):

    collection_title = serializers.CharField(source='collection.collection_title', read_only=True)
    collection_key = serializers.CharField(source='collection.collection_key', read_only=True)
    doc_creator_id = serializers.IntegerField(source='doc_creator.id', read_only=True)
    doc_creator_full_name = serializers.CharField(source='doc_creator.get_full_name', read_only=True)

    class Meta:
        model = Document
        fields = [
            'id',
            'doc_key',
            'doc_title',
            'doc_body',
            'doc_creator_id',
            'doc_creator_full_name',
            'doc_status',
            'created_at',
            'updated_at',            
            'published_at',            
            'collection_title',
            'collection_key',
        ]

class DocumentDetailSerializer(serializers.ModelSerializer):

    collection_title = serializers.CharField(source='collection.collection_title', read_only=True)
    collection_key = serializers.CharField(source='collection.collection_key', read_only=True)
    doc_creator_id = serializers.IntegerField(source='doc_creator.id', read_only=True)
    doc_creator_full_name = serializers.CharField(source='doc_creator.get_full_name', read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = [
            'id',
            'doc_key',
            'doc_title',
            'doc_body',
            'doc_creator_id',
            'doc_creator_full_name',
            'doc_status',
            'created_at',
            'updated_at',            
            'published_at',            
            'collection_title',
            'collection_key',
            'attachments',
        ]

class DocumentTinySerializer(serializers.ModelSerializer):
    doc_creator_id = serializers.IntegerField(source='doc_creator.id', read_only=True)
    doc_creator_full_name = serializers.CharField(source='doc_creator.get_full_name', read_only=True)
    class Meta:
        model = Document
        fields = [
            'id',
            'doc_key',
            'doc_title',
            'doc_body',
            'doc_status',
            'doc_creator_id',
            'doc_creator_full_name',
        ]

class DocumentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'id',
            'doc_key',
            'doc_title',
            'doc_body',
            'doc_status',
        ]
        read_only_fields=[
            'id',
            'doc_key',
        ]

