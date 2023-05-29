from django.urls import path,include
from .views import UserView,MessageView,IndexView
from rest_framework.routers import DefaultRouter
from .import routing

router=DefaultRouter()
router.register('index',IndexView,basename='OnlineProfile')
router.register(r'user_list',UserView)
router.register('message_list',MessageView)

urlpatterns=[
    path('',include(router.urls)),
    path('ws/', include(routing.websocket_urlpatterns))
]