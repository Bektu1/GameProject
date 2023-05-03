from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.exceptions import ValidationError
import random
import tkinter as tk


User = get_user_model()


class Product(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, unique=True)
    updated_at = models.DateTimeField(auto_now=True, unique=True)
    image = models.ImageField(upload_to='product', null=True, blank=True)
    tag = models.ManyToManyField("Tag", related_name='product')
  
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['created_at']

    def __str__(self):
        return self.title
    
class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='likes')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = ('user','product')

    def __str__(self) -> str:
        return f'liked by {self.user.username}'
    

class UserProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    #u1 = User.objects.get(id=1)
    #u1.comments.all()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # не существующий коментарий
    updated_at = models.DateTimeField(auto_now=True) # существующий коментарий 
    sub_comment = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null = True)# не обязательно к заполнению blank true
    article = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
    def __str__(self) -> str:
        return f'Комментарий от {self.user.username}'

class Tag(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
    
    def __str__(self) -> str:
        return self.title
    
class Purchase(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posts = models.ForeignKey(Product, blank=True, on_delete=models.CASCADE)

    def clean(self):
        if self.posts.count() > settings.MAX_FAVORITES_POSTS:
            raise ValidationError('Favorites limit exceeded.')
        
    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'


class CoinGame:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=500, height=500)
        self.canvas.pack()

        self.score = 0
        self.score_text = self.canvas.create_text(50, 10, text=f"Score: {self.score}", anchor=tk.NW)

        self.player = self.canvas.create_oval(240, 240, 260, 260, fill='blue')

        self.coins = []
        for i in range(10):
            x = random.randint(0, 480)
            y = random.randint(0, 480)
            coin = self.canvas.create_oval(x, y, x+20, y+20, fill='yellow')
            self.coins.append(coin)

        self.canvas.bind_all('<Up>', self.move_up)
        self.canvas.bind_all('<Down>', self.move_down)
        self.canvas.bind_all('<Left>', self.move_left)
        self.canvas.bind_all('<Right>', self.move_right)

    def move_up(self, event):
        self.canvas.move(self.player, 0, -10)
        self.check_collisions()

    def move_down(self, event):
        self.canvas.move(self.player, 0, 10)
        self.check_collisions()

    def move_left(self, event):
        self.canvas.move(self.player, -10, 0)
        self.check_collisions()

    def move_right(self, event):
        self.canvas.move(self.player, 10, 0)
        self.check_collisions()

    def check_collisions(self):
        player_coords = self.canvas.bbox(self.player)
        for coin in self.coins:
            coin_coords = self.canvas.bbox(coin)
            if player_coords == coin_coords:
                self.canvas.delete(coin)
                self.coins.remove(coin)
                self.score += 1
                self.canvas.itemconfigure(self.score_text, text=f"Score: {self.score}")
                break

root = tk.Tk()
game = CoinGame(root)
root.mainloop()

    
 

    
