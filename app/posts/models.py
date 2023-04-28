from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, unique=True)
    updated_at = models.DateTimeField(auto_now=True, unique=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['created_at']

    def __str__(self):
        return self.title
    
 

    
