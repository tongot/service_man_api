from django.conf.urls import include, url
from . import views
from rest_framework.routers import DefaultRouter
from knox import views as knox_views

router = DefaultRouter()
router.register('account', views.UserAccountViewSet, basename=('user-account'))
router.register('login', views.LoginViewSet, basename='login')

urlpatterns = [
    url('', include(router.urls)),
    url('user/', views.GetUser.as_view()),
    url('confirm-email/', views.ConfirmCode.as_view()),
    url('reset-password/', views.ForgotPassword.as_view()),
    url('change-password/', views.ChangePassword.as_view()),
    url('log_in', views.LoginAPI.as_view()),
    url('logout', knox_views.LogoutView.as_view()),

]
