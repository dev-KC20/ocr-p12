# users/urls.py

from django.urls import path
# from users.views import CreateUserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # path("signup/", CreateUserViewSet.as_view({"get": "create"}), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
