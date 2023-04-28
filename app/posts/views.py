from django.urls import reverse_lazy
from .models import Product
from rest_framework import viewsets
from .serializers import ProductSerializer
from rest_framework import mixins, permissions, viewsets



class Product(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        method = self.request.method
        if method in permissions.SAFE_METHODS:
            self.permission_classes = [permissions.AllowAny]
        elif method in ['POST', 'DELETE', 'UPDATE']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()



