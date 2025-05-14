from ninja import Schema


class UserGymSchema(Schema):
    user_id: int
    gym_id: int
