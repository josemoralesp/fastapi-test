import strawberry


@strawberry.type
class UserSchema:

    id: strawberry.ID
    name: str
    email: str
    phone: str
    password_hash: str


@strawberry.input
class UserInputSchema:

    name: str = strawberry.field(description="The new user name")
    email: str = strawberry.field(description="The new user email")
    phone: str = strawberry.field(description="The new user phone")
    password_hash: str = strawberry.field(description="The password to be encrypted")