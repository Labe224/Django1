from django.shortcuts import render

def home(request):
    return render(request,'livre/index.html')

# Create your views here.
