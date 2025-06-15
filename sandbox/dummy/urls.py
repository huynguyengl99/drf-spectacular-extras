from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DummyViewSet

router = DefaultRouter()
router.register(r"", DummyViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
