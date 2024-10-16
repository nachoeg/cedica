from src.core.database import db

class TipoDePago(db.Model):
    __tablename__ = "tipo_pago"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True) 

class Pago(db.Model):
    __tablename__ = "pago"

    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Double, nullable=False)
    descripcion = db.Column(db.String(), nullable=False)
    fechaDePago = db.Column(db.String(), nullable=False)

    tipo_id = db.Column(db.Integer, db.ForeignKey('tipo_pago.id'), nullable=False)
    tipo_pago = db.relationship('TipoDePago', backref='pago')

    miembro_id = db.Column(db.Integer, db.ForeignKey('miembro.id'), nullable=False)
    miembro = db.relationship('Miembro', backref='pago')

    def __repr__(self):
        return f'<Pago #{self.id} monto="{self.monto}" fecha="{self.fechaDePago}" descripcion={self.descripcion}'
