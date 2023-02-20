from django.urls import path
from .views import (
    DocumentCreateView,
    DocumentDetailView,
    DocumentListView,
    UpdateDocumentStatusView,
    UpdateDocumentView,
)

urlpatterns = [    
    path('create', DocumentCreateView.as_view()),
    path('list', DocumentListView.as_view()),
    path('<str:doc_key>', DocumentDetailView.as_view(), name="document-detail"),
    path('update-status/<str:doc_key>', UpdateDocumentStatusView.as_view()),
    path('update-doc/<str:doc_key>', UpdateDocumentView.as_view()),
]