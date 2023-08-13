from django.shortcuts import render

# Simulate finch data
finches = [
    {'name': 'Zebra Finch', 'color': 'Black and White', 'size': 'Small'},
    {'name': 'Gouldian Finch', 'color': 'Brightly Colored', 'size': 'Small'},
    {'name': 'Crimson Finch', 'color': 'Red', 'size': 'Small'},
    {'name': 'Society Finch', 'color': 'Various Colors', 'size': 'Small'},
    {'name': 'Lady Gouldian Finch', 'color': 'Brightly Colored', 'size': 'Small'},
]

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    context = {
        'app_description': "Welcome to the Finch Collector application! This app allows you to view information about different finch species.",
    }
    return render(request, 'about.html', context)

def all_finches(request):
    context = {
        'finches': finches,
    }
    return render(request, 'finches/index.html', context)
