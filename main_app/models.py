from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

MEALS = (
    ("B", "Breakfast"),
    ("L", "Lunch"),
    ("D", "Dinner"),
)

class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("toys_detail", kwargs={"pk": self.id})


class Finch(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    toys = models.ManyToManyField(Toy)
    # Add the foreign key linking to a user instance
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.id})"

    # Add this method
    def get_absolute_url(self):
        return reverse("detail", kwargs={"finch_id": self.id})

    def fed_for_today(self):
        print("Today's feedings:", self.feeding_set.filter(date=date.today()))
        print("Total meals:", len(MEALS))
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)


class Photo(models.Model):
  url = models.CharField(max_length=200)
  finch = models.ForeignKey(Finch, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for finch_id: {self.finch_id} @{self.url}"


class Feeding(models.Model):
    date = models.DateField("Feeding Date")
    meal = models.CharField(max_length=1, choices=MEALS, default=MEALS[0][0])

    # Create a finch_id FK
    finch = models.ForeignKey(Finch, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}"

    class Meta:
        ordering = ["-date"]

