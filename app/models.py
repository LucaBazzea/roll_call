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


class BeltBJJ(models.model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    colours = [("white", "White"), ("blue", "Blue"), ("purple", "Purple"), ("brown", "Brown"), ("black", "Black")]
    belt_colour = models.CharField(choices=colours)
    stripes = models.IntegerField(default=0)
