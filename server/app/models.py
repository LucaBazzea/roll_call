from django.db import models


class User(models.Model):
    username = models.CharField(max_length=32, unique=True) # TODO: limit which characters can be used
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)


class Gym(models.Model):
    name = models.CharField(max_length=32)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)


class GymMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    gym = models.ForeignKey(Gym, on_delete=models.PROTECT)
    joined = models.DateTimeField(auto_now_add=True)


class GymTrainingArea(models.Model):
    name = models.CharField(max_length=100)


class Class(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.PROTECT)
    coach = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    days = [("mon", "Monday"), ("tue", "Tuesday"), ("wed", "Wednesday"), ("thu", "Thursday"), ("fri", "Friday"), ("sat", "Saturday"), ("sun", "Sunday")]
    day = models.CharField(choices=days, max_length=9)
    time_start = models.TimeField()
    time_end = models.TimeField()
    colour_hex = models.CharField(max_length=7)
    notes = models.TextField()
    training_area = models.ForeignKey(GymTrainingArea, null=True, on_delete=models.PROTECT)
    cancelled = models.BooleanField(default=False)


class BeltBJJ(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    belt_given_by = models.CharField(null=True, max_length=100)
    colours = [("white", "White"), ("blue", "Blue"), ("purple", "Purple"), ("brown", "Brown"), ("black", "Black")]
    belt_colour = models.CharField(choices=colours, default="white", max_length=6)
    stripes = models.IntegerField(default=0)
