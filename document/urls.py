from django.urls import path
from .views import (
    DocumentCreateView,
    DocumentDetailView,
    DocumentListView,
)

urlpatterns = [    
    path('create', DocumentCreateView.as_view()),
    path('list', DocumentListView.as_view()),
    path('<int:pk>', DocumentDetailView.as_view()),
]