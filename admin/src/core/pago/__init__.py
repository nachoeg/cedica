from src.core.database import db
from src.core.pago.pago import Pago, TipoDePago

def listar_pagos():
    pagos = Pago.query.all()
    return pagos

def crear_pago(**kwargs):
    pago = Pago(**kwargs)
    db.session.add(pago)
    db.session.commit()

    return pago

def listar_tipos_pagos():
    tiposDePagos = TipoDePago.query.all()
    return tiposDePagos

def cargar_tipo_pago(nombre):
    pago = TipoDePago(nombre=nombre)
    db.session.add(pago)
    db.session.commit()
    return pago