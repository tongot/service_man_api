from django.conf.urls import include,url
from . import views
from rest_framework.routers  import DefaultRouter


router = DefaultRouter()
router.register('product-category',views.ProductCategoryView)
router.register('location',views.LocationView)
router.register('product',views.ProductView)
router.register('business',views.BusinessView)
router.register('business-category',views.BusinessCategoryView)
router.register('order',views.OrderView)
router.register('message',views.MessageView)
router.register('product_cover',views.ProductCoverView)
router.register('product-images', views.ProductImagesViewSet, basename='product-images')
router.register('products-own', views.OwnProductViewSet, basename='product-own')
router.register('orders-own', views.OwnBusinessOrderView, basename='orders-own')


urlpatterns = [
    url('',include(router.urls)),
    url('my-business', views.OwnBusinessView.as_view()),

]