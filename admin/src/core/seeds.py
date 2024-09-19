from src.core import auth


def run():
    user1 = auth.create_issue(email="juan@mail.com", alias="Juan", activo=True)
    user2 = auth.create_issue(email="jorge@mail.com", alias="Jorge", activo=False)
    user3 = auth.create_issue(email="maria@mail.com", alias="Maria", activo=True)
