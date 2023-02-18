from django.urls import path
from .views import (
    TokenObtainPairView,    
)

urlpatterns = [

    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'), # <--overridden view; see user.views 
]