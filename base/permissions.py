from rest_framework.permissions import BasePermission
from base.enums import DocumentStatus

class IsSuperUser(BasePermission):
    message = "You are not a superuser. Action restricted."
    def has_permission(self, request, view) -> bool:
        return request.user.is_superuser

class IsStaff(BasePermission):
    message = "You are not an active staff. Action restricted."
    def has_permission(self, request, view):
        return request.user.is_staff and request.user.is_active

class IsActiveMember(BasePermission):
    message = "You are not an active staff. Action restricted."
    def has_permission(self, request, view) -> bool:
        return request.user.is_active 

class IsCollectionOwner(BasePermission):
    # for view permission
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    # for object level permissions
    message = "You are not the owner of this collection. Action restricted."
    def has_object_permission(self, request, view, obj):
        return obj.collection_creator.id == request.user.id

class IsDocumentOwner(BasePermission):
    
    message = "You are not the owner of this document."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.doc_creator.id == request.user.id

class IsDocumentOwnerOrPublishedOrArchived(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        action = ""
        if obj.doc_status == DocumentStatus.DRAFTED.value:
            action = 'drafted'
        elif obj.doc_status == DocumentStatus.DELETED.value:
            action = 'deleted'
        else:
            action = None 

        if obj.doc_status == DocumentStatus.PUBLISHED.value or obj.doc_status == DocumentStatus.ARCHIVED.value:
            return True
        elif obj.doc_creator.id == request.user.id:
            return True
        elif obj.doc_status != DocumentStatus.PUBLISHED.value or obj.doc_status != DocumentStatus.ARCHIVED.value:
            self.message = f"Oops! {request.user.first_name} - the owner has {action} the document."
            return False
        else:
            return False
