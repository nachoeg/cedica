from datetime import datetime
from src.core.database import db

class TipoDePago(db.Model):
    __tablename__ = "tipo_pago"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True) 

class Pago(db.Model):
    __tablename__ = "pago"

    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Double, nullable=False)
    descripcion = db.Column(db.String(), nullable=True)
    fechaDePago = db.Column(db.DateTime, default=datetime.now)

    tipo_id = db.Column(db.Integer, db.ForeignKey('tipo_pago.id'), nullable=False)
    tipo_pago = db.relationship('TipoDePago', backref='pago')

    miembro_id = db.Column(db.Integer, db.ForeignKey('miembro.id'), nullable=True)
    miembro = db.relationship('Miembro', backref='pago')

    def __repr__(self):
        return f'<Pago #{self.id} monto="{self.monto}" fecha="{self.fechaDePago}" descripcion={self.descripcion}'
    
    def to_dict(self):
        return {
            'fechaDePago': self.fechaDePago.strftime('%d-%m-%Y') if self.fechaDePago else None,
            'tipo_pago_nombre': self.tipo_pago.nombre if self.tipo_pago else None,
            'monto': self.monto,
            'descripcion': self.descripcion,  
            'beneficiario': self.miembro.dni if self.miembro and self.miembro.dni else '',
        }
