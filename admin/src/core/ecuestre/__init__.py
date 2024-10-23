from src.core.database import db
from src.core.ecuestre.ecuestre import Ecuestre, TipoDeJyA, TipoDeDocumento, Documento
from src.core.miembro import Miembro, PuestoLaboral
from datetime import datetime


def listar_ecuestres(
    nombre_filtro="",
    tipo_jya_filtro="",
    ordenar_por="id",
    orden="asc",
    pagina=1,
    cant_por_pagina=10,
):
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
    tipos_de_jya = TipoDeJyA.query.all()
    return tipos_de_jya


def listar_tipos_de_documentos():
    tipos_de_documentos = TipoDeDocumento.query.all()
    return tipos_de_documentos


def listar_entrenadores():
    entrenadores = (
        Miembro.query.join(PuestoLaboral, Miembro.puesto_laboral_id == PuestoLaboral.id)
        .filter(PuestoLaboral.nombre == "Entrenador de Caballos")
        .all()
    )
    return entrenadores


def listar_conductores():
    conductores = (
        Miembro.query.join(PuestoLaboral)
        .filter(PuestoLaboral.nombre == "Conductor")
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
    tipo_de_jya = TipoDeJyA(**kwargs)
    db.session.add(tipo_de_jya)
    db.session.commit()
    return tipo_de_jya


def crear_tipo_de_documento(**kwargs):
    tipo_de_documento = TipoDeDocumento(**kwargs)
    db.session.add(tipo_de_documento)
    db.session.commit()
    return tipo_de_documento


def crear_documento(nombre, tipo_de_documento_id, url, ecuestre_id, archivo_externo):
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
    ecuestre = Ecuestre.query.get_or_404(id)
    db.session.delete(ecuestre)
    db.session.commit()
    return ecuestre


def eliminar_tipo_de_jya(tipo_de_jya_id):
    tipo_de_jya = TipoDeJyA.query.get(tipo_de_jya_id)
    db.session.delete(tipo_de_jya)
    db.session.commit()
    return tipo_de_jya


def eliminar_documento_ecuestre(documento_id):
    documento = Documento.query.get(documento_id)
    db.session.delete(documento)
    db.session.commit()
    return documento


def obtener_ecuestre(ecuestre_id):
    ecuestre = Ecuestre.query.get(ecuestre_id)
    return ecuestre


def obtener_tipo_de_jya(tipo_de_jya_id):
    tipo_de_jya = TipoDeJyA.query.get(tipo_de_jya_id)
    return tipo_de_jya


def obtener_documento(documento_id):
    documento = Documento.query.get(documento_id)
    return documento


def asignar_conductor(ecuestre, conductor):
    ecuestre.conductores.append(conductor)
    db.session.commit()
    return ecuestre


def asignar_entrenador(ecuestre, entrenador):
    ecuestre.entrenadores.append(entrenador)
    db.session.commit()
    return ecuestre


def guardar_cambios():
    db.session.commit()
