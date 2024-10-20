from src.core.database import db
from src.core.ecuestre.ecuestre import Ecuestre, TipoDeJyA


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


def listar_tipos_de_jya():
    tipos_de_jya = TipoDeJyA.query.all()
    return tipos_de_jya


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
    )
    db.session.add(ecuestre)
    db.session.commit()
    return ecuestre


def crear_tipo_de_jya(**kwargs):
    tipo_de_jya = TipoDeJyA(**kwargs)
    db.session.add(tipo_de_jya)
    db.session.commit()
    return tipo_de_jya


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


def obtener_ecuestre(ecuestre_id):
    ecuestre = Ecuestre.query.get(ecuestre_id)
    return ecuestre


def obtener_tipo_de_jya(tipo_de_jya_id):
    tipo_de_jya = TipoDeJyA.query.get(tipo_de_jya_id)
    return tipo_de_jya


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
