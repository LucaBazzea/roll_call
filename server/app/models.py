from logging import getHandlerByName
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
    roles = {"owner": "Owner", "admin": "Admin"}
    role = models.CharField(max_length=5, choices=roles, null=True)


class Class(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.PROTECT)
    title = models.CharField(max_length=20)
    coach = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    days = [("mon", "mon"), ("tue", "tue"), ("wed", "wed"), ("thu", "thu"), ("fri", "fri"), ("sat", "sat"), ("sun", "sun")]
    day = models.CharField(choices=days, max_length=9)
    time_start = models.TimeField()
    time_end = models.TimeField()
    capacity = models.PositiveSmallIntegerField(null=True, default=None)
    colour_hex = models.CharField(max_length=7, null=True)
    notes = models.TextField(null=True)
    cancelled = models.BooleanField(default=False)


class ClassBooking(models.Model):
    classe = models.ForeignKey(Class, on_delete=models.PROTECT)
    gym_member = models.ForeignKey(GymMember, on_delete=models.PROTECT)
    class_date = models.DateField(null=True) # TODO: Remove null
    date_created = models.DateTimeField(auto_now_add=True)


class BeltBJJ(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    belt_given_by = models.CharField(null=True, max_length=100)
    colours = [("white", "White"), ("blue", "Blue"), ("purple", "Purple"), ("brown", "Brown"), ("black", "Black")]
    belt_colour = models.CharField(choices=colours, default="white", max_length=6)
    stripes = models.IntegerField(default=0)
