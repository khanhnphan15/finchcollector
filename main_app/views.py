from django.shortcuts import render
from .models import Finch  # Import the Finch model

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    context = {
        'app_description': "Welcome to the Finch Collector application! This app allows you to view information about different finch species.",
    }
    return render(request, 'about.html', context)

# def all_finches(request):
#     finches = Finch.objects.all()
#     context = {
#         'finches': finches,
#     }
#     return render(request, 'finches/index.html', context)

def finches_index(request):
    finches = Finch.objects.all()
    for i in finches:
        a = 'a'
    return render(request, 'finches/index.html', {
        'finches': finches
    })

def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    return render(request, 'finches/detail.html', {
        'finch': finch
    })



