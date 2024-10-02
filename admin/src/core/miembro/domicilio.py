from src.core.database import db


class Domicilio(db.Model):
    __tablename__ = "domicilio"
    id = db.Column(db.Integer, primary_key=True)
    calle = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    piso = db.Column(db.String(10), nullable=True)
    dpto = db.Column(db.String(10), nullable=True)
    localidad = db.Column(db.String(100), nullable=False)
    miembros = db.relationship('Miembro', backref='domicilio', lazy=True)
