from src.core.database import db
from src.core.contacto.consulta import Consulta
from sqlalchemy import cast, String


def listar_consultas(
    estado_filtro="",
    ordenar_por="id",
    orden="asc",
    pagina=1,
    cant_por_pagina=10,
):
    """
    Retorna el listado paginado, filtrado y ordenado de las consultas.
    """

    query = Consulta.query.filter(
        cast(Consulta.estado, String).ilike(f"%{estado_filtro}%")
    )

    cant_resultados = query.count()

    if orden == "asc":
        query = query.order_by(getattr(Consulta, ordenar_por).asc())
    else:
        query = query.order_by(getattr(Consulta, ordenar_por).desc())

    consultas = query.paginate(page=pagina, per_page=cant_por_pagina, error_out=False)
    return consultas, cant_resultados


def listar_estados_consultas():
    """
    Retorna los estados de las consultas.
    """
    return Consulta.Estado.listar()


def crear_consulta(nombre, email, mensaje):
    """
    Crea una consulta.
    """
    consulta = Consulta(
        nombre=nombre,
        email=email,
        mensaje=mensaje,
    )
    db.session.add(consulta)
    db.session.commit()
    return consulta


def eliminar_consulta(consulta_id):
    """
    Elimina una consulta.
    """
    consulta = Consulta.query.get_or_404(consulta_id)
    db.session.delete(consulta)
    db.session.commit()
    return consulta


def guardar_cambios():
    """
    Funcion que guarda los cambios en la base de datos.
    """
    db.session.commit()

def obtener_consulta(id):
    """Funcion que busca una consulta por su id"""
    consulta = Consulta.query.filter_by(id=id).first()
    return consulta