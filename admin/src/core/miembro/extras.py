from src.core.database import db


class Profesion(db.Model):
    __tablename__ = "profesion"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True) 
    
    
class PuestoLaboral(db.Model):
    __tablename__ = "puesto_laboral"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True) 

    
class CondicionDeTrabajo(db.Model):
    __tablename__ = "condicion_trabajo"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)