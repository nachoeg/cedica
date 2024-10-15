from src.core.database import db
from src.core.ecuestre.ecuestre import Ecuestre, TipoDeJyA


def listar_ecuestres():
    ecuestres = Ecuestre.query.all()
    return ecuestres


def listar_tipos_de_jya():
    tipos_de_jya = TipoDeJyA.query.all()
    return tipos_de_jya


def crear_ecuestre(**kwargs):
    ecuestre = Ecuestre(**kwargs)
    db.session.add(ecuestre)
    db.session.commit()
    return ecuestre


def crear_tipo_de_jya(**kwargs):
    tipo_de_jya = TipoDeJyA(**kwargs)
    db.session.add(tipo_de_jya)
    db.session.commit()
    return tipo_de_jya


def eliminar_ecuestre(ecuestre_id):
    ecuestre = Ecuestre.query.get(ecuestre_id)
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


def actualizar_ecuestre(ecuestre_id, **kwargs):
    ecuestre = Ecuestre.query.get(ecuestre_id)
    for key, value in kwargs.items():
        setattr(ecuestre, key, value)
    db.session.commit()
    return ecuestre


def actualizar_tipo_de_jya(tipo_de_jya_id, **kwargs):
    tipo_de_jya = TipoDeJyA.query.get(tipo_de_jya_id)
    for key, value in kwargs.items():
        setattr(tipo_de_jya, key, value)
    db.session.commit()
    return tipo_de_jya
