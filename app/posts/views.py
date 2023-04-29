from django.shortcuts import render, redirect
from django.urls import reverse_lazy 
from .models import Product,Like,Comment,Tag,Purchase
from rest_framework import viewsets,permissions
from .serializers import ProductSerializer,CommentSerializer,TagSerializer,PurchaseSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthor
from rest_framework.pagination import LimitOffsetPagination
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404




class Product(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(methods = ['POST', 'GET'], detail=True)
    def Like(self, request, pk=None):
        product = self.get_object()  # получаем статью
        if not request.user.is_authenticated:
            return Response({'Liked': False, 'Error': 'User not authenticated'})
        like = Like.objects.filter(user=request.user.id, product=product)
        if Like.objects.filter(product=product, user=request.user).exists():
            like.delete()  # если существует, то удали его
            return Response({'Liked': False})
        else:
            Like.objects.create(user=request.user, product=product)
            return Response({'Liked': True})

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated] #передан ли токен 
        elif self.action in ['update','destroy']:
            self.permission_classes = [IsAuthor]  # автор ли он коментария 
        return super().get_permissions()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
    
class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PurchaseView(ModelViewSet):
    queryset = Purchase.objects.all() # Update queryset to be a queryset
    serializer_class = PurchaseSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.BasePermission]

    def post(self, request, *args, **kwargs):
        try:
            post_id = request.data.get('id')
            if post_id is not None:
            # Получение соответствующего экземпляра Post по post_id
                post = Product.objects.get(id=post_id)
            else:
                pass
        except IntegrityError as e:
            pass

            # Создание нового экземпляра Favorites с указанием значения post
            favorite = Purchase.objects.create(posts=post)
        post = get_object_or_404(Product, id=post_id)

        favorite = Purchase.objects.create(
            user=request.user,
            post=post
        )

        serializer = PurchaseSerializer(favorite)
        return Response(serializer.data)

    

    def get(self, request, *args, **kwargs):
        queryset = Purchase.objects.filter(user=request.user)
        paginated_queryset = self.paginate_queryset(queryset, request)
        serializer = PurchaseSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)
