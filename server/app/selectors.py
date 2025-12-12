from app import models


def get_gyms_by_user(user_id):
    return models.GymMember.objects.filter(user_id=user_id)
