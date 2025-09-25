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
    gym_id: int
    title: str
    day: str
    time_start: datetime.time
    time_end: datetime.time
    capacity: int | None = None
    colour_hex: str | None = None
    description: str | None = None
    coach: str | None = None
