from datetime import datetime
from src.core.miembro.miembro import Miembro
from src.core.database import db
from src.core.pago.pago import Pago, TipoDePago

def listar_pagos(
    fecha_inicio="",
    fecha_fin="",
    tipo_pago_id="",
    beneficiario="",
    ordenar_por="fecha_pago",
    orden="asc",
    pagina=1,
    cant_por_pagina=6,
):
    """ Funcion que lista todos los pagos de forma pagina, con un cantidad predefinida
    de 10 pagos por pagina"""
    query = Pago.query.join(TipoDePago).join(Miembro, isouter=True)

    if fecha_inicio:
        query = query.filter(Pago.fecha_pago >= datetime.strptime(fecha_inicio, '%Y-%m-%d'))
    if fecha_fin:
        query = query.filter(Pago.fecha_pago <= datetime.strptime(fecha_fin, '%Y-%m-%d'))
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
    """Crea un pago y lo guarda en la base de datos"""
    pago = Pago(**kwargs)
    db.session.add(pago)
    db.session.commit()
    return pago

def listar_tipos_pagos():
    """Lista los diferentes tipos de pagos que estan cargados en el sistema"""
    tiposDePagos = TipoDePago.query.all()
    return tiposDePagos

def cargar_tipo_pago(nombre):
    """Carga un tipo de pago nuevo"""
    pago = TipoDePago(nombre=nombre)
    db.session.add(pago)
    db.session.commit()
    return pago

def guardar_cambios():
    db.session.commit()

def obtener_pago(id):
    """ Obtiene un pago a partir del id"""
    pago = Pago.query.get_or_404(id)
    return pago

def obtener_tipo_pago(id):
    tipo_pago = TipoDePago.query.get_or_404(id)
    """Obtiene un tipo de pago a partir del id"""
    return tipo_pago

def eliminar_pago(id):
    """Elimina un pago, buscando por id el pago en la base de datos"""
    pago = Pago.query.get_or_404(id)
    db.session.delete(pago)
    db.session.commit()
