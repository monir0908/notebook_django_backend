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
    CollectionSerializer,
    CollectionTinySerializer,
)
from base.permissions import (
    IsActiveMember, 
    IsStaff, 
    IsSuperUser,
    IsCollectionOwner,
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

        if request.data['collection_title'] is None:
            request.data['collection_title'] = "Untitled"
        request.data['collection_creator'] = self.request.user.id

        serializer = CreateCollectionSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):

            serializer.save()

            return JsonResponse(status=status.HTTP_201_CREATED, data={  
                "success": True,
                "state": "success",
                "message": "Collection created successfully!",
                "data": serializer.data
            })


# COLLECTION RETRIEVAL
class CollectionListView(ListAPIView):

    serializer_class = CollectionSerializer
    pagination_class = CustomPagination    

    def get_queryset(self):       

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
    permission_classes = [IsCollectionOwner,]
    # lookup_url_kwarg = "pk"
    lookup_field = 'collection_key'

class UpdateCollectionView(UpdateAPIView): 
    queryset = Collection.objects.all()
    serializer_class = CollectionTinySerializer
    lookup_field = 'collection_key'
    permission_classes = (IsCollectionOwner, )

    def patch(self, request, *args, **kwargs):         
        super(UpdateCollectionView, self).patch(request, *args, **kwargs)
        return JsonResponse(status=status.HTTP_200_OK, data={
            "success": True,
            "warning": False,
            "state": "success",
            "message": "Collection updated...",
        })

