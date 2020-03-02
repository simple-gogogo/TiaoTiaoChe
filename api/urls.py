from django.urls import path
from rest_framework.routers import SimpleRouter

from api.views import *

urlpatterns = [
    path('photos/', upload_car_photo),
    path('tokens/', login),
    path('tokens/<str:token>/', logout),
    path('mobile/<str:tel>/', get_code_by_sms),
    path('districts/', get_provinces),
    path('districts/<int:distid>/', get_district),
    path('hotcities/', HotCityView.as_view()),
]

router = SimpleRouter()
router.register('cartypes', CarTypeViewSet)
router.register('CarShops', CarShopViewSet)
router.register('agents', AgentViewSet)
router.register('tags', TagViewSet)
router.register('carinfos', CarInfoViewSet)
# router.register('users', UserViewSet)
urlpatterns += router.urls