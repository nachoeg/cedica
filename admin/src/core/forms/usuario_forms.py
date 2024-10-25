from flask_wtf import FlaskForm
from wtforms import (BooleanField, EmailField, PasswordField,
                     SelectMultipleField, StringField)
from wtforms.validators import (Email, InputRequired, Length)
from wtforms.widgets import html_params
from core.forms.validaciones import Unico, valor_en_opciones
from core.usuarios import get_roles
from core.usuarios.usuario import Usuario


def select_multi_checkbox(field, ul_class='', **kwargs):
    """Devuelve un widget personalizado de selección múltiple
    en el que cada opción es una checkbox.
    """
    kwargs.setdefault('type', 'checkbox')
    field_id = kwargs.pop('id', field.id)
    html = ['<ul %s>' % html_params(id=field_id, class_=ul_class)]
    for value, label, checked, render_kw in field.iter_choices():
        choice_id = '%s-%s' % (field_id, value)
        options = dict(kwargs, name=field.name, value=value, id=choice_id)
        if checked:
            options['checked'] = 'checked'
        html.append('<li><input %s /> ' % html_params(**options))
        html.append('<label for="%s">%s</label></li>' % (choice_id, label))
    html.append('</ul>')
    return ''.join(html)


class IniciarSesionForm(FlaskForm):
    """Clase que hereda de FlaskForm y representa el formulario
    un usuario sin el campo 'contraseña'.
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
    """Clase que hereda de FlaskForm y representa el formulario
    un usuario sin el campo 'contraseña'.
    """
    email = EmailField("Email", validators=[
        InputRequired("Debe ingresar un email."),
        Email("El mail debe contener '@' y '.'"),
        Unico(Usuario, Usuario.email, message="El mail ingresado ya existe"),
        ])
    alias = StringField("Alias", validators=[
        Unico(Usuario, Usuario.alias, message="El alias ingresado ya existe"),
        ])
    admin_sistema = BooleanField("¿Es admin general?", default=False)
    roles = SelectMultipleField("Roles", widget=select_multi_checkbox,
                                coerce=int)

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
                    Length(min=4, message="La contraseña debe tener por lo \
                        menos %(min)d caracteres")
                    ]
        )
