from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    CustomTokenObtainPairSerializer,
)
# Create your views here.
class TokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer