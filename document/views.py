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
    DocumentUpdateSerializer,
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
    DestroyAPIView,
)


# from system utils
import datetime
date = datetime.date.today()

from django.utils import timezone
now = timezone.now()

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
                "state": "warning",
                "message": "collection property is missing; provide collection property!"
            }) 
        if request.data['collection'] is None:
            return JsonResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={   
                "warning": True,
                "success": False,
                "state": "warning",
                "message": "collection id is missing; provide collection id!"
            }) 


        request.data['doc_title'] = "Untitled"
        request.data['doc_creator'] = self.request.user.id

        serializer = CreateDocumentSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):

            serializer.save()

            return JsonResponse(status=status.HTTP_201_CREATED, data={    
                "success": True,
                "state": "success",
                "message": "Document created successfully!",
                "data": serializer.data
            })

# DOCUMENT RETRIEVAL
class DocumentListView(ListAPIView):

    serializer_class = DocumentSerializer
    pagination_class = CustomPagination    

    def get_queryset(self):       

        order_by_query_param = self.request.query_params.get('order_by', None)

        date_range_str = self.request.query_params.get('date_range_str', None)
        

        if order_by_query_param is not None:
            queryset =  Document.objects.order_by(order_by_query_param)    
        else:
            queryset =  Document.objects.order_by('-id')  
        
        search_param = self.request.query_params.get('search_param', None)
        creator_id = self.request.query_params.get('creator_id', None)    

        if search_param is not None and creator_id is not None:            
            queryset = queryset.filter(
                Q(doc_title__icontains=search_param) |
                Q(doc_body__icontains=search_param),
                Q(doc_creator = creator_id)
            )
        
     
        if creator_id is not None:
            queryset = queryset.filter(doc_creator = creator_id)
        
        collection_id = self.request.query_params.get('collection_id', None) 
        if collection_id is not None:          
            queryset = queryset.filter(collection = collection_id)   

  
        collection_key = self.request.query_params.get('collection_key', None) 
        if collection_key is not None:          
            queryset = queryset.filter(collection_key = collection_key)         

     
        doc_status = self.request.query_params.getlist('doc_status', [])        # using getlist() in case of multiple 'doc_status' request 
        if len(doc_status) > 0:
            queryset = queryset.filter(doc_status__in= doc_status)                # using 'doc_status__in' assuming multiple 'doc_status' request  


        # FILTERING WITH DATE-RANGE - NEED TO REWRITE FOR OPTIMIZATION        

        if date_range_str == 'yesterday':
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            queryset = queryset.filter(updated_at__date=yesterday)
        
        if date_range_str == 'week':
            start = datetime.date.today() - datetime.timedelta(days=7)
            end = start + datetime.timedelta(7)
            queryset = queryset.filter(updated_at__range=[start, end])

        if date_range_str == 'month':
            start = datetime.date.today() - datetime.timedelta(days=30)
            end = datetime.date.today() 
            queryset.filter(updated_at__range=[start, end])
        
        if date_range_str == 'year':
            start = datetime.date.today() - datetime.timedelta(days=365)
            end = datetime.date.today() 
            queryset.filter(updated_at__range=[start, end])


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
                "success":False,
                "warning":True,
                "state": "warning",
                "message":"Apparently, the status is same. Action is aborted.",
            })
        
        action = ""
        if request.data['doc_status'] == DocumentStatus.DRAFTED.value:
            action = 'drafted'
        elif request.data['doc_status'] == DocumentStatus.PUBLISHED.value:
            action = 'published'
            request.data['published_at'] = now
        elif request.data['doc_status'] == DocumentStatus.DELETED.value:
            action = 'deleted'
        elif request.data['doc_status'] == DocumentStatus.ARCHIVED.value:
            action = 'archived'
        else:
            action = None  

        super(UpdateDocumentStatusView, self).patch(request, *args, **kwargs)
        return JsonResponse(status=status.HTTP_200_OK, data={
            "success": True,
            "warning": False,
            "state": "success",
            "message": f"Your document has been {action}.",
        })
class UpdateDocumentView(UpdateAPIView): 
    queryset = Document.objects.all()
    serializer_class = DocumentUpdateSerializer
    lookup_field = 'doc_key'
    permission_classes = (IsDocumentOwner, )

    def patch(self, request, *args, **kwargs):         
        super(UpdateDocumentView, self).patch(request, *args, **kwargs)
        return JsonResponse(status=status.HTTP_200_OK, data={
            "success": True,
            "warning": False,
            "state": "success",
            "message": "Document updated...",
        })
    
# DOCUMENT DELETE
class DeleteDocumentView(DestroyAPIView):

    # this api is used, in case of deleting from database; 
    # normally deleteion only updates status; see 'UpdateDocumentStatusView'


    serializer_class = DocumentSerializer
    queryset = Document.objects.all()
    # permission_classes = (IsDocumentOwner, )

    def delete(self, request, *args, **kwargs):
        super(DeleteDocumentView, self).delete(request, *args, **kwargs)
        return JsonResponse(status=status.HTTP_204_NO_CONTENT, data={
            "state": "success",
            "message": "Document deleted...",
        })