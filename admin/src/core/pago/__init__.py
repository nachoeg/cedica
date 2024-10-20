from datetime import datetime
from src.core.miembro.miembro import Miembro
from src.core.database import db
from src.core.pago.pago import Pago, TipoDePago

def listar_pagos(
    fecha_inicio="",
    fecha_fin="",
    tipo_pago_id="",
    beneficiario="",
    ordenar_por="fechaDePago",
    orden="asc",
    pagina=1,
    cant_por_pagina=10,
):
    query = Pago.query.join(TipoDePago).join(Miembro, isouter=True)

    if fecha_inicio:
        query = query.filter(Pago.fechaDePago >= datetime.strptime(fecha_inicio, '%Y-%m-%d'))
    if fecha_fin:
        query = query.filter(Pago.fechaDePago <= datetime.strptime(fecha_fin, '%Y-%m-%d'))
    if tipo_pago_id:
        pago_tipo = TipoDePago.query.filter_by(nombre=tipo_pago_id).first()
        query = query.filter(Pago.tipo_id == pago_tipo.id)
    if beneficiario:
        query = query.filter(Miembro.dni == int(beneficiario))

    cant_resultados = query.count()

    if orden == "asc":
        query = query.order_by(getattr(Pago, ordenar_por).asc())
    else:
        query = query.order_by(getattr(Pago, ordenar_por).desc())

    pagos = query.paginate(page=pagina, per_page=cant_por_pagina, error_out=False)
    return pagos, cant_resultados

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

def guardar_cambios():
    db.session.commit()

def obtener_pago(id):
    pago = Pago.query.get(id)
    return pago