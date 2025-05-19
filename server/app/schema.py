from ninja import Schema


class UserGymSchema(Schema):
    user_id: int
    gym_id: int


ClassBookingSchema(Schema):
    user_id: int
    gym_id: int
    class_id: int
