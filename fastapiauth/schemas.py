import strawberry


@strawberry.type
class UserSchema:

    id: strawberry.ID
    username: str
    password_hash: str


@strawberry.input
class UserInputSchema:

    username: str = strawberry.field(description="The new of the new user")
    password_hash: str = strawberry.field(description="The password to be encrypted")