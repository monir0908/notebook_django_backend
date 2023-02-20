from django.urls import path
from .views import (
    CreateCollectionView,
    CollectionListView,
    CollectionDetailView,
    UpdateCollectionView,
)

urlpatterns = [
    path('create', CreateCollectionView.as_view()),
    path('list', CollectionListView.as_view()),
    path('<str:collection_key>', CollectionDetailView.as_view()),
    path('update-collection/<str:collection_key>', UpdateCollectionView.as_view()),
]