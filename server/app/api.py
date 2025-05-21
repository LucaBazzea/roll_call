from datetime import datetime

from django.db.models import Q
from django.core.cache import cache

from ninja import NinjaAPI
from ninja.responses import Response

from app import models, schema


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


@api.post("/schedule/")
def get_schedule(request, data: schema.UserGymSchema):
    try:
        models.GymMember.objects.get(user_id=data.user_id, gym_id=data.gym_id).exists()
    except models.GymMember.DoesNotExist:
        return Response({"message": "User / gym not found"}, status=404)

    schedule = {
        "mon": [],
        "tue": [],
        "wed": [],
        "thu": [],
        "fri": [],
        "sat": [],
        "sun": []
    }

    classes = models.Class.objects.get(gym_id=data.gym_id)
    for row in classes:
        classe = {"title": row.title, "start": row.time_start,
                  "end": row.time_end, "colour": row.colour_hex, "coach": row.coach}
        schedule[row.day].append(classe)

    return Response(schedule, status=200)


@api.post("/class/book/")
def class_book(request, data: schema.ClassBookingSchema):
    # Check if user is part of the gym that the class belongs to
    try:
        gym_member_id = models.GymMember.objects.get(user_id=data.user_id, gym_id=data.gym_id).id
    except models.GymMember.DoesNotExist:
        return Response({"message": "User / gym not found"}, status=404)

    try:
        classe = models.Class.objects.get(id=data.class_id).values("id", "capacity")
    except models.Class.DoesNotExist:
        return Response({"message": "Class not found"}, status=402)

    class_bookings_count = models.ClassBooking.objects.filter(classe__id=data.class_id).count()
    if classe["capacity"] != None:
        if classe["capacity"] <= class_bookings_count:
            return Response({"message": "Class full"}, status=403)

    new_booking = models.ClassBooking(
        classe_id = data.class_id,
        gym_member_id = gym_member_id
    )
    new_booking.save()

    return Response({"message": "Class booking created successfully"}, status=200)
