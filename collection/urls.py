from django.urls import path
from .views import (
    CreateCollectionView,
    CollectionListView,
    CollectionDetailView,
)

urlpatterns = [
    path('create', CreateCollectionView.as_view()),
    path('list', CollectionListView.as_view()),
    path('<int:pk>', CollectionDetailView.as_view()),
]