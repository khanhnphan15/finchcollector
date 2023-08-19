import os
import uuid
import boto3
from django.shortcuts import redirect, render
# Add UpdateView & DeleteView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Finch, Toy, Photo  # Import the Finch model
from .forms import FeedingForm
from datetime import date


@login_required
def add_photo(request, finch_id):
    # photo-file maps to the "name" attr on the <input>
    photo_file = request.FILES.get("photo-file", None)
    if photo_file:
        s3 = boto3.client("s3")
        # Need a unique "key" (filename)
        # It needs to keep the same file extension
        # of the file that was uploaded (.png, .jpeg, etc.)
        key = 'projects-6-5/' + uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind(".") :]
        try:
            bucket = os.environ["BUCKET_NAME"]
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, finch_id=finch_id)
        except Exception as e:
            print('An error occured uploading to s3, probably wrong url, bucket name or keys code ~/.aws/credentials is where your keys are')
            print(e)
    return redirect("detail", finch_id=finch_id)


# Create your views here.
def home(request):
    return render(request, "home.html")


def about(request):
    context = {
        "app_description": "Welcome to the Finch Collector application! This app allows you to view information about different finch species.",
    }
    return render(request, "about.html", context)


@login_required
def finches_index(request):
    finches = Finch.objects.filter(user=request.user)
    for i in finches:
        a = "a"
    return render(request, "finches/index.html", {"finches": finches})


@login_required
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
    # This inherited method is called when a
    # valid cat form is being submitted


def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
    return super().form_valid(form)


class FinchUpdate(LoginRequiredMixin, UpdateView):
    model = Finch
    # Let's disallow the renaming of a finch by excluding the name field!
    fields = ["breed", "color", "description", "age"]


class FinchDelete(LoginRequiredMixin, DeleteView):
    model = Finch
    success_url = "/finches"


@login_required
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


class ToyList(LoginRequiredMixin, ListView):
    model = Toy


class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy


class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = "__all__"


class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ["name", "color"]


class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = "/toys"


@login_required
def assoc_toy(request, finch_id, toy_id):
    # Note that you can pass a toy's id instead of the whole toy object
    Finch.objects.get(id=finch_id).toys.add(toy_id)
    return redirect("detail", finch_id=finch_id)


@login_required
def unassoc_toy(request, finch_id, toy_id):
    # Note that you can pass a toy's id instead of the whole toy object
    Finch.objects.get(id=finch_id).toys.remove(toy_id)
    return redirect("detail", finch_id=finch_id)

def signup(request):
    error_message = ""
    if request.method == "POST":
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect("index")
        else:
            error_message = "Invalid sign up - try again"
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "registration/signup.html", context)
