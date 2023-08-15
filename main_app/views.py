from django.shortcuts import redirect, render

# Add UpdateView & DeleteView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Finch, Toy  # Import the Finch model
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


def finches_index(request):
    finches = Finch.objects.all()
    for i in finches:
        a = "a"
    return render(request, "finches/index.html", {"finches": finches})


def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    # First, create a list of the toy ids that the finch DOES have
    id_list = finch.toys.all().values_list("id")
    toys_finch_doesnt_have = Toy.objects.exclude(id__in=id_list)
    # instantiate FeedingForm to be rendered in the template
    feeding_form = FeedingForm()
    return render(
        request,
        "finches/detail.html",
        {"finch": finch, "feeding_form": feeding_form, "toys": toys_finch_doesnt_have},
    )


class FinchCreate(CreateView):
    model = Finch
    fields = ["name", "color", "breed", "description", "age"]
    #   or fields = '__all__'
    # Special string pattern Django will use
    # success_url = "/finches/{finch_id}"
    # Or if you wanted to redirect to the index page
    # success_url = '/finches'


class FinchUpdate(UpdateView):
    model = Finch
    # Let's disallow the renaming of a finch by excluding the name field!
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
    return redirect("detail", finch_id=finch_id)

class ToyList(ListView):
    model = Toy

class ToyDetail(DetailView):
    model = Toy

class ToyCreate(CreateView):
    model = Toy
    fields = "__all__"

class ToyUpdate(UpdateView):
    model = Toy
    fields = ["name", "color"]

class ToyDelete(DeleteView):
    model = Toy
    success_url = "/toys"

def assoc_toy(request, finch_id, toy_id):
    # Note that you can pass a toy's id instead of the whole toy object
    Finch.objects.get(id=finch_id).toys.add(toy_id)
    return redirect("detail", finch_id=finch_id)

def unassoc_toy(request, finch_id, toy_id):
    # Note that you can pass a toy's id instead of the whole toy object
    Finch.objects.get(id=finch_id).toys.remove(toy_id)
    return redirect("detail", finch_id=finch_id)
