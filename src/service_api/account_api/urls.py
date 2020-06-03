from django.conf.urls import include,url
from . import views
from rest_framework.routers  import DefaultRouter

router = DefaultRouter()
router.register('account', views.UserAccountViewSet, basename=('user-account'))
router.register('login',views.LoginViewSet, basename='login')

urlpatterns = [
    url('',include(router.urls)),
    url('user/',views.GetUser.as_view())
]
