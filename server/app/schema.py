import datetime

from ninja import Schema


class GymSchema(Schema):
    gym_id: int


class GymMemberSchema(Schema):
    user_id: int
    gym_id: int


class ClassBookingSchema(Schema):
    gym_id: int
    class_id: int


class GymClassSchema(Schema):
    gym_id: int
    class_id: int

class ClassSchema(Schema):
    title: str
    day: str
    time_start: datetime.time
    time_end: datetime.time
    capacity: int
    colour_hex: str
    notes: str
    coach_user_id: int | None = None
