from django.urls import path
from .views import (
    DocumentCreateView,
    DocumentDetailView,
    DocumentListView,
    DocumentListSharedWithMeView,
    UpdateDocumentStatusView,
    UpdateDocumentView,
    DeleteDocumentView,
    AttachmentUploadView,
    DeleteAttachmentView,
)

urlpatterns = [    
    path('create', DocumentCreateView.as_view()),
    path('list', DocumentListView.as_view()),
    path('list-shared-with-me', DocumentListSharedWithMeView.as_view()),
    path('<str:doc_key>', DocumentDetailView.as_view(), name="document-detail"),
    path('update-status/<str:doc_key>', UpdateDocumentStatusView.as_view()),
    path('update-doc/<str:doc_key>', UpdateDocumentView.as_view()),
    path('delete-doc/<int:pk>', DeleteDocumentView.as_view()),
    path('upload-attachment/<int:pk>', AttachmentUploadView.as_view()), # document pk
    path('delete-attachment/<int:pk>', DeleteAttachmentView.as_view()), # attachment pk
]