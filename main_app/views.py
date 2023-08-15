from django.shortcuts import redirect, render
# Add UpdateView & DeleteView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Finch  # Import the Finch model
from .forms import FeedingForm
from datetime import date

# Create your views here.
def home(request):
    return render(request, "home.html")

def about(request):
    context = {
        "app_description": "Welcome to the Finch Collector application! This app allows you to view information about different finch species.",
    }
    return render(request, "about.html", context)

# def all_finches(request):
#     finches = Finch.objects.all()
#     context = {
#         'finches': finches,
#     }
#     return render(request, 'finches/index.html', context)

def finches_index(request):
    finches = Finch.objects.all()
    for i in finches:
        a = "a"
    return render(request, "finches/index.html", {"finches": finches})

def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    # instantiate FeedingForm to be rendered in the template
    feeding_form = FeedingForm()
    return render(
        request, "finches/detail.html", {"finch": finch, "feeding_form": feeding_form}
    )

class FinchCreate(CreateView):
    model = Finch
    fields = "__all__"
    #   or fields = ['name', 'color', 'breed', 'description', 'age']
    # Special string pattern Django will use
    # success_url = "/finches/{finch_id}"
    # Or if you wanted to redirect to the index page
    # success_url = '/cats'

class FinchUpdate(UpdateView):
    model = Finch
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ["breed", "color", "description", "age"]

class FinchDelete(DeleteView):
    model = Finch
    success_url = "/finches"
    
def add_feeding(request, finch_id):
  # create a ModelForm instance using 
  # the data that was submitted in the form
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # We want a model instance, but
    # we can't save to the db yet
    # because we have not assigned the
    # finch_id FK.
    new_feeding = form.save(commit=False)
    new_feeding.finch_id = finch_id
    new_feeding.date = date.today()  # Set the date to today's date
    new_feeding.save()
  return redirect('detail', finch_id=finch_id)
