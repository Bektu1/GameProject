from django.shortcuts import render
from models import TkinterApp

def tkinter_view(request):
    app = TkinterApp()
    return render(request, 'tkinter_template.html', {'app': app})


# Create your views here.
