from src.core.database import db
from datetime import datetime
import enum
from sqlalchemy.types import Enum
from flask_sqlalchemy import SQLAlchemy
class Cobro(db.Model):
    __tablename__ = "cobros"

    class MedioDePago(enum.Enum):
        efectivo = "Efectivo"
        credito = "Tarjeta de crédito"
        debito = "Tarjeta de débito"
        otro = "Otro medio de pago"

        def __str__(self):
            return f'{self.value}'

    id = db.Column(db.Integer, primary_key=True)
    fecha_pago = db.Column(db.DateTime, default=datetime.now)
    medio_de_pago = db.Column(Enum(MedioDePago))
    monto = db.Column(db.Double, nullable=False)
    observaciones = db.Column(db.String(100))
    #recibio_el_dinero(referencia a tabla de miembros)
    joa_id = db.Column(db.Integer, db.ForeignKey('jinetesyamazonas.id'))

    joa = db.relationship('JineteOAmazona')

    '''
        Método que devuelve los resultados paginados dada la pagina y la cantidad de elementos por página.
        El parámetro asc se utiliza para que, si se le pasa de manera explícita un 0 como parámetro, 
        se devuelvan los resultados de manera descendente
    '''
    @staticmethod
    def todos_paginados(asc=1, pagina=1, por_pagina=2):
        if asc == 0:
                return Cobro.query.order_by(Cobro.fecha_pago.desc()).paginate(page=pagina, per_page=por_pagina)
        else:
            return Cobro.query.order_by(Cobro.fecha_pago.asc()).paginate(page=pagina, per_page=por_pagina)


    def __repr__(self):
        return f'<Cobro #{self.id} fecha de pago={self.fecha_pago}, medio de pago: {self.medio_de_pago}, observaciones: "{self.observaciones}">'