from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import Product,CommentViewSet,TagViewSet,PurchaseView
# from .views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView

# urlpatterns = [
#     path('', ProductListView.as_view(), name='product_list'),
#     path('create/', ProductCreateView.as_view(), name='product_create'),
#     path('<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
#     path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
# ]


router = DefaultRouter()
router.register('product', Product, 'product'),
router.register('comment', CommentViewSet, 'comments'),
router.register('tags', TagViewSet, 'tags'),
router.register(r'purchase', PurchaseView, basename='purchase')
urlpatterns = router.urls