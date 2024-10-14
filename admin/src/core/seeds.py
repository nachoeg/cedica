from src.core import auth
from src.core import ecuestre


def run():
    user1 = auth.create_user(email="juan@mail.com", alias="Juan", activo=True)
    user2 = auth.create_user(email="jorge@mail.com", alias="Jorge", activo=False)
    user3 = auth.create_user(email="maria@mail.com", alias="Maria", activo=True)

    tipos_de_jya = [
        "Hipoterapia",
        "Monta Terapéutica",
        "Deporte Ecuestre Adaptado",
        "Actividades Recreativas",
        "Equitación",
    ]

    for tipo in tipos_de_jya:
        ecuestre.crear_tipo_de_jya(tipo=tipo)

    ecuestre1 = ecuestre.crear_ecuestre(
        nombre="Caballo1",
        fecha_nacimiento="2020-01-01",
        sexo="M",
        raza="Criollo",
        pelaje="Tostado",
        es_compra=True,
        fecha_ingreso="2020-01-01",
        sede="Sede1",
        tipo_de_jya_id=1,
    )
    ecuestre2 = ecuestre.crear_ecuestre(
        nombre="Caballo2",
        fecha_nacimiento="2012-05-10",
        sexo="F",
        raza="Criollo",
        pelaje="Tostado",
        es_compra=False,
        fecha_ingreso="2020-01-01",
        sede="Sede2",
        tipo_de_jya_id=2,
    )
