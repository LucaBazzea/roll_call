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
