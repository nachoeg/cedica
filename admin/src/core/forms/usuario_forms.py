from flask_wtf import FlaskForm
from wtforms import (BooleanField, EmailField, PasswordField,
                     SelectMultipleField, StringField)
from wtforms.validators import (Email, InputRequired, Length, EqualTo)
from core.forms.validaciones import (Unico, sin_espacios,
                                     validar_contraseña, valor_en_opciones)
from core.usuarios import get_roles
from core.usuarios.usuario import Usuario


class IniciarSesionForm(FlaskForm):
    """Clase que hereda de FlaskForm y representa el formulario
    que permite al usuario iniciar sesión con email y contraseña.
    """
    email = EmailField(
        "Email",
        validators=[
            InputRequired("Debe ingresar un email."),
            Email("El mail debe contener '@' y '.'"),
        ])
    contraseña = PasswordField(
        "Contraseña",
        validators=[InputRequired("Debe ingresar una contraseña.")],
        )


class UsuarioSinContraseñaForm(FlaskForm):
    """Clase que hereda de FlaskForm y representa el formulario de
    un usuario sin el campo 'contraseña'.
    """
    email = EmailField("Email", validators=[
        InputRequired("Debe ingresar un email."),
        Length(max=100, message="No puedo tener más de %(max)d caracteres."),
        Email("El mail debe contener '@' y '.'"),
        Unico(Usuario, Usuario.email, ilike=True, message="El mail ingresado ya existe."),
        ])
    alias = StringField("Alias", validators=[
        InputRequired("Debe ingresar un alias."),
        Length(max=100, message="No puedo tener más de %(max)d caracteres."),
        Unico(Usuario, Usuario.alias, ilike=True, message="El alias ingresado ya existe."),
        sin_espacios,
        ])
    admin_sistema = BooleanField("¿Es admin general?", default=False)
    roles = SelectMultipleField("Roles", coerce=int)

    def __init__(self, *args, **kwargs):
        """Construye los atributos necesarios para la
        clase UsuarioSinContraseñaForm.
        """
        super(UsuarioSinContraseñaForm, self).__init__(*args, **kwargs)
        # carga las opciones al campo roles
        opciones = [(rol.id, rol.nombre) for rol in get_roles()]
        self.roles.choices = opciones
        # agrega validación de que el valor recibido está entre las opciones
        id_opciones = [opcion[0] for opcion in self.roles.choices]
        self.roles.validators = [valor_en_opciones(id_opciones)]


class UsuarioForm(UsuarioSinContraseñaForm):
    """Clase que hereda de UsuarioSinContraseñaForm y representa
    el formulario de un usuario.
    """
    contraseña = PasswordField(
        "Contraseña",
        validators=[InputRequired("Debe ingresar una contraseña."),
                    Length(min=4, max=100, message="La contraseña debe \
                           tener por lo menos %(min)d caracteres."),
                    sin_espacios,
                    ]
        )


class CambiarContraseñaForm(FlaskForm):
    """Clase que hereda de FlaskForm y representa el formulario
    que le permite a un usuario cambiar su contraseña.
    """
    contraseña_anterior = PasswordField(
        "Contraseña anterior",
        validators=[InputRequired("Debe ingresar su contraseña."),
                    Length(min=4, max=100, message="La contraseña \
                           tiene por lo menos %(min)d caracteres."),
                    sin_espacios,
                    ]
        )
    contraseña_nueva = PasswordField(
        "Nueva contraseña",
        validators=[InputRequired("Debe ingresar una contraseña."),
                    Length(min=4, max=100, message="La contraseña debe \
                           tener por lo menos %(min)d caracteres."),
                    sin_espacios,
                    ]
        )
    contraseña_confirmacion = PasswordField(
        "Reingrese la nueva contraseña",
        validators=[InputRequired("Debe ingresar de nuevo la contraseña."),
                    EqualTo('contraseña_nueva', message="Las contraseñas deben coincidir")
                    ]
        )

    def __init__(self, contraseña, *args, **kwargs):
        """Construye los atributos necesarios para la
        clase CambiarContraseñaForm.
        """
        super().__init__(*args, **kwargs)
        # agrega validación de contraseña contra la que se recibe como parámetro
        self.contraseña_anterior.validators = [validar_contraseña(contraseña)]
