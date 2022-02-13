from graphene import String, ObjectType, Int


class UserSchema(ObjectType):

    id = Int(required=True)
    username = String(required=True)
    password_hash = String()
