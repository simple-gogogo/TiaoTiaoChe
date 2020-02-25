from django.urls import path
from rest_framework.routers import SimpleRouter

from api.views import get_provinces, get_district, HotCityView, \
    AgentViewSet, carTypeViewSet, car_shopViewSet, TagViewSet, carInfoViewSet

urlpatterns = [
    path('districts/', get_provinces),
    path('districts/<int:distid>/', get_district),
    path('hotcities/', HotCityView.as_view()),
]

router = SimpleRouter()
router.register('cartypes', carTypeViewSet)
router.register('car_shops', car_shopViewSet)
router.register('agents', AgentViewSet)
router.register('tags', TagViewSet)
router.register('carinfos', carInfoViewSet)
urlpatterns += router.urls
