from src.core import auth


def run():
    user1 = auth.create_user(email="juan@mail.com", alias="Juan", activo=True)
    user2 = auth.create_user(email="jorge@mail.com", alias="Jorge", activo=False)
    user3 = auth.create_user(email="maria@mail.com", alias="Maria", activo=True)
