from django.urls import path
from .views import (
    LoginView,
    SignUpView,
    ProfilePicUpdateView,
)

urlpatterns = [

    path('login', LoginView.as_view(), name='token_obtain_pair'), # <--overridden view; see user.views 
    path('signup', SignUpView.as_view()),
    path('update-profile-pic/<int:pk>', ProfilePicUpdateView.as_view(), name='update-profile-pic'),
]