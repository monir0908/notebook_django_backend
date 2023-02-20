from django.urls import path
from .views import (
    DocumentCreateView,
    DocumentDetailView,
    DocumentListView,
)

urlpatterns = [    
    path('create', DocumentCreateView.as_view()),
    path('list', DocumentListView.as_view()),
    path('<str:doc_key>', DocumentDetailView.as_view()),
]