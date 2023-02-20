from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status
from base.pagination import CustomPagination
from .models import Document
from base.enums import DocumentStatus

from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat

from .serializers import (    
    CreateDocumentSerializer,
    DocumentTinySerializer,
    DocumentSerializer,
)
from base.permissions import (
    IsSuperUser,
    IsStaff, 
    IsActiveMember, 
    IsDocumentOwner,
    IsDocumentOwnerOrPublishedOrArchived,
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

        prop = "collection"

        if not prop in request.data.keys():
            print("collection id is missing; provide collection key!") 
            return JsonResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={   
                "warning": True,
                "success": False,
                "message": "collection property is missing; provide collection property!"
            }) 
        if request.data['collection'] is None:
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

        # 2. FILTERING WITH DOCUMENT STATUS
        doc_status = self.request.query_params.get('doc_status', None)         
        if doc_status is not None:
            queryset = queryset.filter(doc_status= doc_status)

        return queryset
class DocumentDetailView(RetrieveAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsDocumentOwnerOrPublishedOrArchived, ]
    # lookup_url_kwarg = "pk"
    lookup_field = 'doc_key'

# DOCUMENT UPDATE
class UpdateDocumentStatusView(UpdateAPIView): 
    queryset = Document.objects.all()
    serializer_class = CreateDocumentSerializer
    lookup_field = 'doc_key'
    permission_classes = (IsDocumentOwner, )

    def patch(self, request, *args, **kwargs):
        existing_obj: Document = self.get_object()
        
        
        if existing_obj.doc_status == request.data['doc_status']: # checking sent status and exiting status is same.
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={
                "sucess":False,
                "warning":True,
                "message":"Apparently, the status is same. Action is aborted.",
            })
        
        action = ""
        if request.data['doc_status'] == DocumentStatus.DRAFTED.value:
            action = 'drafted'
        elif request.data['doc_status'] == DocumentStatus.PUBLISHED.value:
            action = 'published'
        elif request.data['doc_status'] == DocumentStatus.DELETED.value:
            action = 'deleted'
        elif request.data['doc_status'] == DocumentStatus.ARCHIVED.value:
            action = 'archived'
        else:
            action = None  

        super(UpdateDocumentStatusView, self).patch(request, *args, **kwargs)
        return JsonResponse(status=status.HTTP_200_OK, data={
            "sucess": True,
            "warning": False,
            "message": f"Your document has been {action}.",
        })
class UpdateDocumentView(UpdateAPIView): 
    queryset = Document.objects.all()
    serializer_class = DocumentTinySerializer
    lookup_field = 'doc_key'
    permission_classes = (IsDocumentOwner, )

    def patch(self, request, *args, **kwargs):         
        super(UpdateDocumentView, self).patch(request, *args, **kwargs)
        return JsonResponse(status=status.HTTP_200_OK, data={
            "sucess": True,
            "warning": False,
            "message": "Document updated...",
        })