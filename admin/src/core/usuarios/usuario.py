from datetime import datetime
from src.core.database import db


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    contraseña = db.Column(db.String(100), nullable=False)
    alias = db.Column(db.String(100), nullable=False, unique=True)
    activo = db.Column(db.Boolean, nullable=False)
    admin_sistema = db.Column(db.Boolean, default=False, nullable=False)
    creacion = db.Column(db.DateTime, default=datetime.now)
    ultima_actualizacion = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    roles = db.relationship('Rol', secondary='roles_usuario', lazy=True, backref=db.backref('usuarios', lazy=False))

    def __repr__(self):
        return f'<Usuario #{self.id} email={self.email} alias={self.alias} activo={self.activo}>'


class Rol(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    permisos = db.relationship('Permiso', secondary='permisos_rol', lazy=True, backref=db.backref('roles', lazy=True))

    def __repr__(self):
        return f'<Rol #{self.id} nombre={self.nombre}>'


class Permiso(db.Model):
    __tablename__ = "permisos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f'<Permiso #{self.id} nombre={self.nombre}>'


# tabla intermedia para la relación muchos a muchos entre usuarios y roles
roles_usuario = db.Table('roles_usuario', 
                         db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True), 
                         db.Column('rol_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
                         )

# tabla intermedia para la relación muchos a muchos entre roles y permisos
permisos_rol = db.Table('permisos_rol', 
                        db.Column('rol_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True), 
                        db.Column('permiso_id', db.Integer, db.ForeignKey('permisos.id'), primary_key=True)
                        )
