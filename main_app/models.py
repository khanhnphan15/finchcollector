from django.db import models
from django.urls import reverse
from datetime import date

MEALS = (
    ("B", "Breakfast"),
    ("L", "Lunch"),
    ("D", "Dinner"),
)


class Finch(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.id})"

    # Add this method
    def get_absolute_url(self):
        return reverse("detail", kwargs={"finch_id": self.id})

    def fed_for_today(self):
        print("Today's feedings:", self.feeding_set.filter(date=date.today()))
        print("Total meals:", len(MEALS))
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)


class Feeding(models.Model):
    date = models.DateField("Feeding Date")
    meal = models.CharField(max_length=1, choices=MEALS, default=MEALS[0][0])

    # Create a finch_id FK
    finch = models.ForeignKey(Finch, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}"

    class Meta:
        ordering = ["-date"]
