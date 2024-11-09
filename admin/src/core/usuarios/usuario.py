from datetime import datetime
from src.core.database import db
from src.web.handlers.funciones_auxiliares import (booleano_a_palabra,
                                                   fechahora_a_fecha)


class Usuario(db.Model):
    """Clase que representa un usuario del sistema."""
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    contraseña = db.Column(db.String(100), nullable=False)
    alias = db.Column(db.String(100), nullable=False, unique=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    admin_sistema = db.Column(db.Boolean, default=False, nullable=False)
    creacion = db.Column(db.DateTime, default=datetime.now)
    ultima_actualizacion = db.Column(db.DateTime, default=datetime.now,
                                     onupdate=datetime.now)

    roles = db.relationship('Rol', secondary='roles_usuario', lazy=True,
                            backref=db.backref('usuarios', lazy=False))

    def to_dict(self):
        """Método que devuelve un diccionario con los datos
        del usuario: alias, email, activo, fecha_creacion,
        admin_sistema y roles."

        """
        return {
            "alias": self.alias,
            "email": self.email,
            "activo": booleano_a_palabra(self.activo),
            "creacion": fechahora_a_fecha(self.creacion),
            "admin_sistema": booleano_a_palabra(self.admin_sistema),
            "roles": "".join(("" + rol.nombre + ". ") for rol in self.roles),
        }

    def __repr__(self):
        """Método que devuelve la representación de un usuario."""
        return f'<Usuario #{self.id} email={self.email} alias={self.alias} \
                  activo={self.activo}>'


class Rol(db.Model):
    """Clase que representa un rol en el sistema."""
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    permisos = db.relationship('Permiso', secondary='permisos_rol', lazy=True,
                               backref=db.backref('roles', lazy=True))

    def __repr__(self):
        """Método que devuelve la representación de un rol."""
        return f'<Rol #{self.id} nombre={self.nombre}>'


class Permiso(db.Model):
    """Clase que representa un permiso en el sistema."""
    __tablename__ = "permisos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        """Método que devuelve la representación de un permiso."""
        return f'<Permiso #{self.id} nombre={self.nombre}>'


# tabla intermedia para la relación muchos a muchos entre usuarios y roles
roles_usuario = db.Table('roles_usuario',
                         db.Column('usuario_id',
                                   db.Integer,
                                   db.ForeignKey('usuarios.id'),
                                   primary_key=True),
                         db.Column('rol_id',
                                   db.Integer,
                                   db.ForeignKey('roles.id'),
                                   primary_key=True)
                         )

# tabla intermedia para la relación muchos a muchos entre roles y permisos
permisos_rol = db.Table('permisos_rol',
                        db.Column('rol_id',
                                  db.Integer,
                                  db.ForeignKey('roles.id'),
                                  primary_key=True),
                        db.Column('permiso_id',
                                  db.Integer,
                                  db.ForeignKey('permisos.id'),
                                  primary_key=True)
                        )
