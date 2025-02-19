from django.db.models import Q
from django.core.cache import cache

from ninja import NinjaAPI
from ninja.responses import Response

from app import models, schema, services


api = NinjaAPI()


# TODO: Return gym info
@api.get("/user/")
def get_user(request, id: int):
    try:
        user = models.User.objects.get(id=id)
    except models.User.DoesNotExist:
        return 404

    try:
        belt_bjj_query = models.BeltBJJ.objects.get(user=user)

        belt_bjj = {
            "colour": belt_bjj_query.belt_colour,
            "stripes": belt_bjj_query.stripes
        }
    except:
        belt_bjj = None

    response = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "belt_bjj": belt_bjj
    }

    return response
