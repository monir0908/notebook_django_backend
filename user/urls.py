from django.urls import path
from .views import (
    LoginView,
    SignUpView,
)

urlpatterns = [

    path('login', LoginView.as_view(), name='token_obtain_pair'), # <--overridden view; see user.views 
    path('signup', SignUpView.as_view()),
]