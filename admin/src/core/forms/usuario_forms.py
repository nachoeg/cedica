from flask_wtf import FlaskForm
from wtforms import (BooleanField, EmailField, PasswordField,
                     SelectMultipleField, StringField)
from wtforms.validators import (Email, InputRequired, Length,
                                ValidationError, AnyOf)
from wtforms.widgets import html_params
from src.core.database import db
from core.usuarios.usuario import Rol, Usuario


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


class Unique(object):
    """Validador que verifica que el valor del campo
     sea único si se modificó.
     """
    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if message is None:
            message = u'Este valor ya existe'
        self.message = message

    def __call__(self, form, field):
        """Permite llamar a la clase como una función"""
        if field.object_data == field.data:
            return
        check = db.session.execute(db.select(self.model).where(
            self.field == field.data)).scalars().all()
        if check:
            raise ValidationError(self.message)


# def validar_email(form, field):
#     validacion = re.match(
#         r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', field.data)
#     if not validacion:
#         raise ValidationError("El mail debe contener '@' y '.'")


def opcion_en_opciones(opciones):
    """Función que valida que los id de roles seleccionados estén entre
    las opciones.
    """
    mensaje = "El valor selecionado no está entre las opciones válidas."

    def _length(form, field):
        if not set(field.data).issubset(set(opciones)):
            raise ValidationError(mensaje)

    return _length


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
        Unique(Usuario, Usuario.email, message="El mail ingresado ya existe"),
        ])
    alias = StringField("Alias", validators=[
        Unique(Usuario, Usuario.alias, message="El alias ingresado ya existe"),
        ])
    admin_sistema = BooleanField("¿Es admin general?", default=False)
    roles = SelectMultipleField("Roles", widget=select_multi_checkbox, )

    def __init__(self, *args, **kwargs):
        """Construye los atributos necesarios para la
        clase UsuarioSinContraseñaForm.
        """
        super(UsuarioSinContraseñaForm, self).__init__(*args, **kwargs)
        opciones = [
            (rol.id, rol.nombre) for rol in
            db.session.execute(db.select(Rol)).unique().scalars().all()
            ]
        self.roles.choices = opciones
        id_opciones = [str(opcion[0]) for opcion in self.roles.choices]
        self.roles.validators = [opcion_en_opciones(id_opciones)]


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
