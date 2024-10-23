from src.core.usuarios import todos_alias, todos_emails
from flask_wtf import FlaskForm
from wtforms import (BooleanField, EmailField, PasswordField,
                     SelectMultipleField, StringField)
from wtforms.validators import Email, InputRequired, Length, ValidationError
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
        if field.object_data == field.data:
            return
        check = db.session.execute(db.select(self.model).where(self.field == field.data)).scalars().all()
        # raise Exception(f'{check}')
        # check = DBSession.query(model).filter(field == data).first()
        if check:
            raise ValidationError(self.message)


class UsuarioSinContraseñaForm(FlaskForm):
    email = EmailField("Email", validators=[
        InputRequired("El formato del email no es correcto."),
        Email(),
        Unique(Usuario, Usuario.email, message="El mail ingresado ya existe"),
        ])
    alias = StringField("Alias", validators=[
        Unique(Usuario, Usuario.alias, message="El alias ingresado ya existe"),
        ])
    admin_sistema = BooleanField("¿Es admin general?", default=False)
    roles = SelectMultipleField("Roles", widget=select_multi_checkbox)

    def __init__(self, *args, **kwargs):
        super(UsuarioSinContraseñaForm, self).__init__(*args, **kwargs)
        self.roles.choices = [
            (rol.id, rol.nombre) for rol in
            db.session.execute(db.select(Rol)).unique().scalars().all()
            ]


class UsuarioForm(UsuarioSinContraseñaForm):
    contraseña = PasswordField(
        "Contraseña",
        validators=[InputRequired(),
                    Length(min=4, message="La contraseña debe tener por lo \
                        menos %(min)d caracteres")
                    ]
        )
