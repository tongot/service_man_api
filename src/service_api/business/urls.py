from django.conf.urls import include,url
from . import views
from rest_framework.routers  import DefaultRouter


router = DefaultRouter()
router.register('product-category',views.ProductCategoryView)
router.register('country', views.CountryView)
router.register('location',views.LocationView)
router.register('product',views.ProductView,basename='product')
router.register('business',views.BusinessView,basename='business')
router.register('business-category',views.BusinessCategoryView)
router.register('order',views.OrderView)
router.register('message',views.MessageView)
router.register('product_cover',views.ProductCoverView)
router.register('business_profiles',views.BusinessProfileView)
router.register('product-images', views.ProductImagesViewSet, basename='product-images')
router.register('products-own', views.OwnProductViewSet, basename='product-own')
router.register('orders-own', views.OwnBusinessOrderView, basename='orders-own')
router.register('rate-business', views.BusinessRatingView, basename='rate-business')
router.register('business-comment', views.BusinessCommentView, basename='business-comment')
router.register('replycomment-business', views.BusinessCommentReplyView, basename='replycomment-business')

urlpatterns = [
    url('',include(router.urls)),
    url('my-business', views.OwnBusinessView.as_view()),

]