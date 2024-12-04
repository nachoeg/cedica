from src.core.database import db
from src.core.ecuestre.ecuestre import Ecuestre, TipoDeJyA, TipoDeDocumento, Documento
from src.core.miembro import Miembro, PuestoLaboral
from datetime import datetime
from sqlalchemy.exc import IntegrityError


def listar_ecuestres(
    nombre_filtro="",
    tipo_jya_filtro="",
    ordenar_por="id",
    orden="asc",
    pagina=1,
    cant_por_pagina=10,
):
    """
    Retorna el listado paginado, filtrado y ordenado de los ecuestres.
    """
    query = Ecuestre.query.join(TipoDeJyA).filter(
        Ecuestre.nombre.ilike(f"%{nombre_filtro}%"),
        TipoDeJyA.tipo.ilike(f"%{tipo_jya_filtro}%"),
    )

    cant_resultados = query.count()

    if orden == "asc":
        query = query.order_by(getattr(Ecuestre, ordenar_por).asc())
    else:
        query = query.order_by(getattr(Ecuestre, ordenar_por).desc())

    ecuestres = query.paginate(page=pagina, per_page=cant_por_pagina, error_out=False)
    return ecuestres, cant_resultados


def listar_documentos(
    ecuestre_id,
    nombre_filtro="",
    tipo_filtro="",
    ordenar_por="id",
    orden="asc",
    pagina=1,
    cant_por_pagina=10,
):
    """
    Retorna el listado paginado, filtrado y ordenado de los documentos de un ecuestre.
    """
    query = Documento.query.join(TipoDeDocumento).filter(
        Documento.ecuestre_id == ecuestre_id,
        Documento.nombre.ilike(f"%{nombre_filtro}%"),
        TipoDeDocumento.tipo.ilike(f"%{tipo_filtro}%"),
    )

    cant_resultados = query.count()

    if orden == "asc":
        query = query.order_by(getattr(Documento, ordenar_por).asc())
    else:
        query = query.order_by(getattr(Documento, ordenar_por).desc())

    documentos = query.paginate(page=pagina, per_page=cant_por_pagina, error_out=False)
    return documentos, cant_resultados


def listar_tipos_de_jya():
    """
    Retorna el listado de los tipos de jinetes y amazonas.
    """
    tipos_de_jya = TipoDeJyA.query.all()
    return tipos_de_jya


def listar_tipos_de_documentos():
    """
    Retorna el listado de los tipos de documentos de ecuestres.
    """
    tipos_de_documentos = TipoDeDocumento.query.all()
    return tipos_de_documentos


def listar_entrenadores():
    """
    Retorna el listado de los miembros que son entrenadores de caballos y están activos.
    """
    entrenadores = (
        Miembro.query.join(PuestoLaboral, Miembro.puesto_laboral_id == PuestoLaboral.id)
        .filter(
            PuestoLaboral.nombre == "Entrenador de Caballos", Miembro.activo == True
        )
        .all()
    )
    return entrenadores


def listar_conductores():
    """
    Retorna el listado de los miembros que son conductores de caballos y están activos.
    """
    conductores = (
        Miembro.query.join(PuestoLaboral, Miembro.puesto_laboral_id == PuestoLaboral.id)
        .filter(PuestoLaboral.nombre == "Conductor", Miembro.activo == True)
        .all()
    )
    return conductores


def crear_ecuestre(
    nombre,
    fecha_nacimiento,
    sexo,
    raza,
    pelaje,
    es_compra,
    fecha_ingreso,
    sede,
    tipo_de_jya_id,
    conductores,
    entrenadores,
):
    """
    Crea un objeto de tipo Ecuestre con los datos que recibe por parámetro y lo devuelve.
    """
    ecuestre = Ecuestre(
        nombre=nombre,
        fecha_nacimiento=fecha_nacimiento,
        sexo=sexo,
        raza=raza,
        pelaje=pelaje,
        es_compra=es_compra,
        fecha_ingreso=fecha_ingreso,
        sede=sede,
        tipo_de_jya_id=tipo_de_jya_id,
        conductores=conductores,
        entrenadores=entrenadores,
    )
    db.session.add(ecuestre)
    db.session.commit()
    return ecuestre


def crear_tipo_de_jya(**kwargs):
    """
    Crea un objeto de tipo TipoDeJyA con los datos que recibe por parámetro y lo devuelve.
    """
    tipo_de_jya = TipoDeJyA(**kwargs)
    db.session.add(tipo_de_jya)
    db.session.commit()
    return tipo_de_jya


def crear_tipo_de_documento(**kwargs):
    """
    Crea un objeto de tipo TipoDeDocumento con los datos que recibe por parámetro y lo devuelve.
    """
    tipo_de_documento = TipoDeDocumento(**kwargs)
    db.session.add(tipo_de_documento)
    db.session.commit()
    return tipo_de_documento


def crear_documento(nombre, tipo_de_documento_id, url, ecuestre_id, archivo_externo):
    """
    Crea un objeto de tipo Documento con los datos que recibe por parámetro y lo devuelve.
    """
    documento = Documento(
        nombre=nombre,
        fecha=datetime.now(),
        tipo_de_documento_id=tipo_de_documento_id,
        url=url,
        ecuestre_id=ecuestre_id,
        archivo_externo=archivo_externo,
    )
    db.session.add(documento)
    db.session.commit()
    return documento


def eliminar_ecuestre(id):
    """
    Funcion que, dado un id, elimina el ecuestre con dicho id.
    """
    ecuestre = Ecuestre.query.get_or_404(id)
    try:
        db.session.delete(ecuestre)
        db.session.commit()
        return ecuestre
    except IntegrityError:
        db.session.rollback()
        raise ValueError(
            "No se puede eliminar el ecuestre porque está asociado a un Jinete o Amazona."
        )


def eliminar_tipo_de_jya(tipo_de_jya_id):
    """
    Funcion que, dado un id, elimina el tipo de jinete o amazona con dicho id.
    """
    tipo_de_jya = TipoDeJyA.query.get(tipo_de_jya_id)
    db.session.delete(tipo_de_jya)
    db.session.commit()
    return tipo_de_jya


def eliminar_documento_ecuestre(documento_id):
    """
    Funcion que, dado un id, elimina el documento de ecuestre con dicho id.
    """
    documento = Documento.query.get(documento_id)
    db.session.delete(documento)
    db.session.commit()
    return documento


def obtener_ecuestre(ecuestre_id):
    """
    Funcion que busca y retorna un ecuestre por su id.
    """
    ecuestre = Ecuestre.query.get(ecuestre_id)
    return ecuestre


def obtener_tipo_de_jya(tipo_de_jya_id):
    """
    Funcion que busca y retorna un tipo de jinete o amazona por su id.
    """
    tipo_de_jya = TipoDeJyA.query.get(tipo_de_jya_id)
    return tipo_de_jya


def obtener_documento(documento_id):
    """
    Funcion que busca y retorna un documento de ecuestre por su id.
    """
    documento = Documento.query.get(documento_id)
    return documento


def asignar_conductor(ecuestre, conductor):
    """
    Agrega un conductor al ecuestre pasado por parámetro.
    """
    ecuestre.conductores.append(conductor)
    db.session.commit()
    return ecuestre


def asignar_entrenador(ecuestre, entrenador):
    """
    Agrega un entrenador al ecuestre pasado por parámetro.
    """
    ecuestre.entrenadores.append(entrenador)
    db.session.commit()
    return ecuestre


def guardar_cambios():
    """
    Funcion que guarda los cambios en la base de datos.
    """
    db.session.commit()
