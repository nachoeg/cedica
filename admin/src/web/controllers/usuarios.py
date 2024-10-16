from flask import Blueprint, flash, redirect, render_template, request, url_for
from core.usuarios import crear_usuario
from core.usuarios.usuario_forms import UsuarioForm

bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@bp.route('/registrar_usuario', methods=['GET', 'POST'])
def registrar_usuario():
    form = UsuarioForm(request.form)
    if form.validate_on_submit():
        # raise Exception(f'{form.roles.data}')
        usuario = crear_usuario(form.email.data, form.contraseña.data, 
                                form.alias.data, form.admin_sistema.data, 
                                form.roles.data)
        flash(f'Se ha registrado correctamente al \
              usuario {usuario.alias}')
        return redirect(url_for('usuarios.registrar_usuario'))
    return render_template('usuarios/registrar_usuario.html', form=form)