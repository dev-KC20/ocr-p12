# # users/urls.py
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework_nested import routers
from .views import ClientViewSet, ContractViewSet, EventViewSet

router = routers.SimpleRouter()
router.register("clients", ClientViewSet, basename="clients")

client_router = routers.NestedSimpleRouter(router, r"clients", lookup="clients")
client_router.register("contracts", ContractViewSet, basename="contracts")
contract_router = routers.NestedSimpleRouter(client_router, r"contracts", lookup="contracts")
contract_router.register("events", EventViewSet, basename="events")

urlpatterns = [
    path("users/login/", TokenObtainPairView.as_view(), name="login"),
    path("", TokenObtainPairView.as_view(), name="login"),
    path("users/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
    path("", include(client_router.urls)),
    path("", include(contract_router.urls)),
]
