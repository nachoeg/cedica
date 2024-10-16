from flask_wtf import FlaskForm
from wtforms import (BooleanField, EmailField, PasswordField,
                     SelectMultipleField, StringField)
from wtforms.validators import Email, InputRequired, Length
from wtforms.widgets import html_params
from src.core.database import db
from core.usuarios.usuario import Rol, Usuario


def select_multi_checkbox(field, ul_class='', **kwargs):
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


def emails():
    emails = db.session.execute(db.select(Usuario.email)).scalars().all()

    return emails


class UsuarioForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired(), Email()])
    contraseña = PasswordField(
        "Contraseña", 
        validators=[InputRequired(), 
                    Length(min=4, message="La contraseña debe tener por lo \
                        menos %(min)d caracteres")
                    ]
        )
    alias = StringField("Alias")
    admin_sistema = BooleanField("¿Es admin general?", default=False)
    roles = SelectMultipleField("Roles", widget=select_multi_checkbox)

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.roles.choices = [
            (rol.id, rol.nombre) for rol in 
            db.session.execute(db.select(Rol)).unique().scalars().all()
            ]
