from api.viewsets import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'animais', AnimalViewSet)