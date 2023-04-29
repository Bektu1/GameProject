from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import Product
from .views import Product,CommentViewSet,TagViewSet,PurchaseView

router = DefaultRouter()
router.register('product', Product, 'product')
router.register('comment', CommentViewSet, 'comments'),
router.register('tags', TagViewSet, 'tags'),
router.register(r'purchase', PurchaseView, basename='purchase')
urlpatterns = router.urls