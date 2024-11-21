from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms.validators import Email, EqualTo, InputRequired, Length

from src.core.forms.validaciones import sin_espacios, validar_contraseña


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


class CambiarContraseñaForm(FlaskForm):
    """Clase que hereda de FlaskForm y representa el formulario
    que le permite a un usuario cambiar su contraseña.
    """
    contraseña_anterior = PasswordField(
        "Contraseña anterior",
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
                    EqualTo('contraseña_nueva', message="Las contraseñas \
                            deben coincidir")
                    ]
        )

    def __init__(self, contraseña, *args, **kwargs):
        """Construye los atributos necesarios para la
        clase CambiarContraseñaForm.
        """
        super().__init__(*args, **kwargs)
        # validación de contraseña contra la que se recibe como parámetro
        self.contraseña_anterior.validators = [
            InputRequired("Debe ingresar su contraseña."),
            Length(min=4, max=100, message="La contraseña \
                   tiene por lo menos %(min)d caracteres."),
            sin_espacios,
            validar_contraseña(contraseña)
            ]
