from datetime import datetime
from src.core.database import db


class Miembro(db.Model):
    __tablename__ = "miembro"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.BigInteger, nullable=False)
    nombre_contacto_emergencia = db.Column(db.String(100), nullable=False)
    telefono_contacto_emergencia = db.Column(db.BigInteger, nullable=False)
    obra_social = db.Column(db.String(100), nullable=True)
    numero_afiliado = db.Column(db.Integer, nullable=False)

    # relacion con condicion
    condicion_id = db.Column(db.Integer, db.ForeignKey('condicion_trabajo.id'), nullable=False)
    condicion_trabajo = db.relationship('CondicionDeTrabajo', backref='miembros')
    
    # relacion con profesion
    profesion_id = db.Column(db.Integer, db.ForeignKey('profesion.id'), nullable=False)
    profesion = db.relationship('Profesion', backref='miembros')   

    # relacion con puesto laboral
    puesto_laboral_id = db.Column(db.Integer, db.ForeignKey('puesto_laboral.id'), nullable=False)
    puesto_laboral = db.relationship('PuestoLaboral', backref='miembros')  

    # relacion con domicilio
    domicilio_id = db.Column(db.Integer, db.ForeignKey('domicilio.id'), nullable=False)
    domicilio = db.relationship('Domicilio', backref='miembros')

    # relacion con usuario
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    usuario = db.relationship('Usuario', backref='miembro', uselist=False)

    fecha_creacion = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f'<Miembro #{self.id} email="{self.email}" alias="{self.alias}" activo={self.activo}'

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'dni': self.dni,
            'email': self.email,
            'telefono': self.telefono,
            'profesion': self.profesion.nombre if self.profesion else None,
            'puesto_laboral': self.puesto_laboral.nombre if self.puesto_laboral else None,
            'fecha_creacion': self.fecha_creacion.strftime('%d-%m-%Y') if self.fecha_creacion else None
        }