from django.contrib import admin
from .models import Product, Like,Comment,Tag
# Register your models here.
admin.site.register([Product,Like,Comment,Tag])
