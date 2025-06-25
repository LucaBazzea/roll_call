from datetime import datetime

from django.db.models import Q
from django.core.cache import cache

from ninja import NinjaAPI
from ninja.responses import Response

from app import models, schema, services

api = NinjaAPI()


@api.get("/user/")
def user(request, data):
    # user_id = request.session.get("user_id")
    user_id = 1

    try:
        models.User.objects.get(user_id=user_id).exists()
    except models.User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)

    try:
        belt_bjj_query = models.BeltBJJ.objects.filter(
            user_id=user_id
        ).values(
            "belt_colour",
            "stripes",
            "belt_given_by"
        ).last()

        belt_bjj = {
            "colour": belt_bjj_query["belt_colour"],
            "stripes": belt_bjj_query["stripes"],
            "belt_given_by": belt_bjj_query["belt_given_by"]
        }
    except:
        belt_bjj = None

    try:
        gyms = models.GymMember.objects.filter(
            user_id=user_id
        ).values(
            "gym__id",
            "gym__name",
        )
    except:
        gyms = None


    response = {
        "id": gym_member.user.id,
        "username": gym_member.user.username,
        "email": gym_member.user.email,
        "belt_bjj": belt_bjj,
        "gyms": gyms
    }

    return response


@api.get("/gym/member/")
def gym_member(request, data):
    # user_id = request.session.get("user_id")
    user_id = 1

    try:
        user = models.GymMember.objects.get(user_id=user_id, gym_id=data.gym_id).values("role")
    except models.GymMember.DoesNotExist:
        return Response({"message": "User not associated with gym"}, status=404)

    try:
        gym_member = models.GymMember.objects.get(user_id=data.user_id, gym_id=data.gym_id)
    except models.GymMember.DoesNotExist:
        return Response({"message": "Gym member not found"}, status=404)

    response = {}
    # Data that only gym owners and admins should be able to see
    if user["role"] is not None:
        response["email"] = gym_member.user.email

    try:
        belt_bjj_query = models.BeltBJJ.objects.filter(
            user_id=gym_member.user.id
        ).values(
            "belt_colour",
            "stripes",
            "belt_given_by"
        ).last()

        belt_bjj = {
            "colour": belt_bjj_query["belt_colour"],
            "stripes": belt_bjj_query["stripes"],
            "belt_given_by": belt_bjj_query["belt_given_by"]
        }
    except:
        belt_bjj = None

    response["id"] = gym_member.user.id,
    response["username"] = gym_member.user.username,
    response["belt_bjj"] = belt_bjj

    return response


@api.post("/admin/class/create/")
def get_schedule_create(request, data: schema.ClassSchema):
    # user_id = request.session.get("user_id")
    user_id = 1

    try:
        gym_member = models.GymMember.objects.get(user_id=user_id, gym_id=data.gym_id).values("role")

        if gym_member["role"] is None:
            return Response({"message": "Invalid permissions"}, status=403)

    except models.GymMember.DoesNotExist:
        return Response({"message": "User / gym not found"}, status=402)

    try:
        class_new = models.Class(
            data.title,
            data.day,
            data.time_start,
            data.time_end,
            data.capacity,
            data.colour_hex,
            data.notes,
            data.cancelled,
            data.coach_user_id
        )
        class_new.save()
    except Exception as error:
        return Response({"Error": error}, status=500)

    return Response({"message": "Class created successfully"}, status=200)


@api.post("/schedule/")
def get_schedule(request, data: schema.GymSchema):
    # user_id = request.session.get("user_id")
    user_id = 1

    try:
        models.GymMember.objects.get(user_id=user_id, gym_id=data.gym_id)
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

    classes = models.Class.objects.filter(
        gym_id=data.gym_id
    ).select_related(
        "coach"
    ).values(
        "id",
        "title",
        "day",
        "time_start",
        "time_end",
        "capacity",
        "colour_hex",
        "notes",
        "cancelled",
        "coach__username"
    )

    bookings = models.ClassBooking.objects.filter(
        classe_id__in=classes.values_list("id", flat=True)
    ).values_list(
        "classe_id",
        flat=True
    )

    for row in classes:
        bookings_count = 0
        for class_id in bookings:
            if class_id == row["id"]:
                bookings_count += 1

        classe = {
            "title": row["title"],
            "start": row["time_start"],
            "end": row["time_end"],
            "capacity": row["capacity"],
            "bookings_count": bookings_count,
            "colour": row["colour_hex"],
            "notes": row["notes"],
            "coach": row["coach__username"]
        }
        schedule[row["day"]].append(classe)

    return Response(schedule, status=200)


@api.post("/class/book/")
def class_book(request, data: schema.ClassBookingSchema):
    # user_id = request.session.get("user_id")
    user_id = 1

    # Check if user is part of the gym that the class belongs to
    try:
        gym_member_id = models.GymMember.objects.get(user_id=user_id, gym_id=data.gym_id).id
    except models.GymMember.DoesNotExist:
        return Response({"message": "User / gym not found"}, status=404)

    try:
        classe = models.Class.objects.get(id=data.class_id).values("id", "day", "capacity")
    except models.Class.DoesNotExist:
        return Response({"message": "Class not found"}, status=402)

    class_bookings_count = models.ClassBooking.objects.filter(classe__id=data.class_id).count()

    # Check if class is full
    if classe["capacity"] is not None:
        if classe["capacity"] <= class_bookings_count:
            return Response({"message": "Class full"}, status=403)

    # Classes don't have dates, but class bookings do
    date_today = datetime.now().date()
    week_current = services.get_week(date_today)
    class_date = week_current[classe["day"]]

    new_booking = models.ClassBooking(
        classe_id=data.class_id,
        gym_member_id=gym_member_id,
        class_date=class_date
    )
    new_booking.save()

    return Response({"message": "Class booking created successfully"}, status=200)


@api.post("/admin/class/get-bookings/")
def get_class_bookings(request, data: schema.GymClassSchema):
    # user_id = request.session.get("user_id")
    user_id = 1

    try:
        gym_member = models.GymMember.objects.get(user_id=user_id, gym_id=data.gym_id).values("role")

        if gym_member["role"] is None:
            return Response({"message": "Invalid permissions"}, status=403)

    except models.GymMember.DoesNotExist:
        return Response({"message": "User / gym not found"}, status=402)

    try:
        classe = models.Class.objects.get(id=data.class_id).values("id", "day")
    except models.Class.DoesNotExist:
        return Response({"message": "Class not found"}, status=405)

    # Classes don't have dates, but class bookings do
    date_today = datetime.now().date()
    week_current = services.get_week(date_today)
    class_date = week_current[classe["day"]]

    bookings = models.ClassBooking.objects.filter(classe_id=classe["id"], class_date=class_date).first()
    return Response(bookings, status=200)

