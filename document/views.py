from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from base.pagination import CustomPagination
from .models import Document

from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat

from .serializers import (    
    CreateDocumentSerializer,
    DocumentSerializer
)
from base.permissions import (
    IsActiveMember, 
    IsStaff, 
    IsSuperUser,
)
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)


# DOCUMENT CREATION
class DocumentCreateView(APIView):
    
    permission_classes =  (IsActiveMember,) 
    
    def post(self,request):

        key = "collection"

        if not key in request.data.keys():
            print("collection id is missing; provide collection key!") 
            return JsonResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={   
                "warning": True,
                "success": False,
                "message": "collection id is missing; provide collection id!"
            })        

        request.data['doc_title'] = "Untitled"
        request.data['doc_creator'] = self.request.user.id

        serializer = CreateDocumentSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):

            serializer.save()

            return JsonResponse(status=status.HTTP_201_CREATED, data={    
                "success": True,
                "message": "Document created successfully!",
                "data": serializer.data
            })

# DOCUMENT RETRIEVAL
class DocumentListView(ListAPIView):

    serializer_class = DocumentSerializer
    pagination_class = CustomPagination    

    def get_queryset(self):       

        # queryset =  BillItems.objects.all().order_by('id')    
        queryset =  Document.objects.order_by('id')    
        
        search_param = self.request.query_params.get('search_param', None)
        if search_param is not None:            
            queryset.filter(
                Q(doc_title__icontains=search_param) |
                Q(doc_body__icontains=search_param) 
            )
        # 1. FILTERING WITH 'collection_id'
        collection_id = self.request.query_params.get('collection_id', None)       
                        
        if collection_id is not None:          
            queryset = queryset.filter(collection = collection_id) 

        return queryset
class DocumentDetailView(RetrieveAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    # lookup_url_kwarg = "pk"
    lookup_field = 'doc_key'