from src.core.database import db
from src.core.contacto.consulta import Consulta, EstadoConsulta, HistorialEstado
from sqlalchemy import cast, String, and_


def listar_consultas(
    estado_filtro="",
    ordenar_por="id",
    orden="asc",
    pagina=1,
    cant_por_pagina=10,
    archivado=True
):
    """
    Retorna el listado paginado, filtrado y ordenado de las consultas.
    """


    query = Consulta.query.filter(
    and_(
        cast(Consulta.estado, String).ilike(f"%{estado_filtro}%"),
        Consulta.archivado == archivado
    )
    )

    cant_resultados = query.count()

    if orden == "asc":
        query = query.order_by(getattr(Consulta, ordenar_por).asc())
    else:
        query = query.order_by(getattr(Consulta, ordenar_por).desc())

    consultas = query.paginate(page=pagina, per_page=cant_por_pagina, error_out=False)
    return consultas, cant_resultados

def listar_historial(
        id,
        pagina=1,
        cant_por_pagina=10,
):
    query = HistorialEstado.query.filter_by(consulta_id=id)
    cant_resultados = query.count()
    consultas = query.paginate(page=pagina, per_page=cant_por_pagina, error_out=False)
    return consultas, cant_resultados

def listar_estados_consultas():
    """
    Retorna los estados de las consultas.
    """
    return EstadoConsulta.listar()


def crear_consulta(titulo, email, mensaje):
    """
    Crea una consulta.
    """
    consulta = Consulta(
        titulo=titulo,
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

def archivar_consulta(id):
    consulta = Consulta.query.filter_by(id=id).first()
    consulta.archivado = True
    db.session.commit()

def desarchivar_consulta(id):
    consulta = Consulta.query.filter_by(id=id).first()
    consulta.archivado = False
    db.session.commit()

def actualizar_estado(id, estado, comentario, usuario):
    consulta = Consulta.query.filter_by(id=id).first()
    crear_historia_estado(consulta.estado, consulta.comentario, consulta.ultimo_editor, consulta.id)
    aux = str(estado).lower()
    consulta.estado = EstadoConsulta[aux]
    consulta.comentario = comentario
    consulta.ultimo_editor = usuario
    db.session.commit()

def crear_historia_estado(estado, comentario, usuario, consulta):
    historial = HistorialEstado(
        estado = estado,
        comentario = comentario,
        usuario = usuario,
        consulta_id = consulta
    )
    db.session.add(historial)
    db.session.commit()
    return historial