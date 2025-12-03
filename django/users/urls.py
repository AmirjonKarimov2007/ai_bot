from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PromocodeViewSet, PromocodeUsageViewSet

router = DefaultRouter()
router.register(r'promocodes', PromocodeViewSet)
router.register(r'promocode-usage', PromocodeUsageViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
