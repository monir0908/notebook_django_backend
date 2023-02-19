from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from base.pagination import CustomPagination
from .models import Collection

from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat

from .serializers import (    
    CreateCollectionSerializer,
    CollectionListSerializer,
    CollectionSerializer,
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


# COLLECTION CREATION
class CreateCollectionView(APIView):

    permission_classes =  (IsActiveMember,) 
    
    def post(self,request):

        request.data['collection_title'] = "Untitled"
        request.data['collection_creator'] = self.request.user.id

        serializer = CreateCollectionSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):

            serializer.save()

            return JsonResponse(status=status.HTTP_201_CREATED, data={  
                "success": True,
                "message": "Collection created successfully!",
                "data": serializer.data
            })


# COLLECTION RETRIEVAL
class CollectionListView(ListAPIView):

    serializer_class = CollectionListSerializer
    pagination_class = CustomPagination    

    def get_queryset(self):       

        # queryset =  BillItems.objects.all().order_by('id')    
        queryset =  Collection.objects.order_by('id')    
        
        search_param = self.request.query_params.get('search_param', None)
        if search_param is not None:            
            queryset.filter(
                Q(collection_title__icontains=search_param) |
                Q(collection_body__icontains=search_param) 
            )
        # 1. FILTERING WITH USER ID 
        creator_id = self.request.query_params.get('creator_id', None)       
                        
        if creator_id is not None:          
            queryset = queryset.filter(collection_creator = creator_id) 

        return queryset
class CollectionDetailView(RetrieveAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    lookup_url_kwarg = "pk"


