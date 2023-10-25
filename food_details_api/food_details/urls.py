from django.urls import path
from .views import FoodTableViewSet, APIInformationView

urlpatterns = [
    path(
        "products/",
        FoodTableViewSet.as_view({"get": "list", "post": "create"}),
        name="foodtable-list",
    ),
    path(
        "products/<str:pk>/",
        FoodTableViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="foodtable-detail",
    ),
    path("info/", APIInformationView.as_view(), name="api_status"),
]
