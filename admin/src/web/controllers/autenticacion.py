from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from src.core.usuarios import (actualizar_perfil, roles_por_usuario,
                               usuario_por_email_y_contraseña, usuario_por_id)
from src.core.usuarios.usuario_forms import UsuarioEditarForm
from src.web.handlers.decoradores import (chequear_usuario_sesion,
                                          sesion_iniciada_requerida)

bp = Blueprint("autenticacion", __name__, url_prefix="")


@bp.route('/iniciar_sesion', methods=('GET', 'POST'))
def iniciar_sesion():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        usuario = usuario_por_email_y_contraseña(email, contraseña)

        if usuario is None:
            flash('Usuario y/o contraseña incorrectos', 'error')

        # es necesario un mensaje distinto al de un usuario que no existe?
        elif not usuario.activo:
            flash('Usuario bloqueado', 'error')

        else:
            session.clear()
            session['usuario'] = usuario.email  # cambiar por session['mail']?
            session['id'] = usuario.id
            session['alias'] = usuario.alias
            session['es_admin'] = usuario.admin_sistema
            session['roles'] = [rol.nombre for rol in usuario.roles]
            flash('Ha iniciado sesión', 'exito')
            return redirect(url_for('home'))

    return render_template('pages/usuarios/iniciar_sesion.html')


@bp.route('/cerrar_sesion')
def cerrar_sesion():
    # raise Exception(f'{session.get('usuario')}')
    del session['usuario']
    session.clear()
    flash('Se ha cerrado la sesión', 'exito')
    return redirect(url_for('home'))


@bp.route('/perfil', methods=['GET'])
@sesion_iniciada_requerida
def ver_perfil():
    usuario = usuario_por_id(session.get('id'))
    return render_template("pages/usuarios/ver_usuario.html", usuario=usuario)


@bp.route('/<int:id>/editar_perfil', methods=['GET', 'POST'])
@chequear_usuario_sesion
@sesion_iniciada_requerida
def editar_perfil(id):
    usuario = usuario_por_id(id)
    form = UsuarioEditarForm(obj=usuario)
    if request.method == 'GET':
        form.roles.data = [str(rol.id) for rol in roles_por_usuario(id)]
    elif form.validate_on_submit():
        # raise Exception(f'{form.data}')
        actualizar_perfil(usuario, form.email.data, form.alias.data)
        flash(f'Se guardaron los cambios al usuario \
              Alias: {usuario.alias}, email: {usuario.email}', 'exito')
        return redirect(url_for('autenticacion.ver_perfil'))
    return render_template('pages/usuarios/editar_perfil.html', form=form)
