from django.urls import path
from views import views

urlpatterns = [
    path('tkinter/', views.tkinter_view, name='tkinter'),
]
