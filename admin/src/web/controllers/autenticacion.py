from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from src.core.usuarios import (actualizar_perfil,
                               usuario_por_email_y_contraseña, usuario_por_id)
from core.forms.usuario_forms import (IniciarSesionForm,
                                      UsuarioSinContraseñaForm)
from src.web.handlers.decoradores import (chequear_usuario_sesion,
                                          sesion_iniciada_requerida)

bp = Blueprint("autenticacion", __name__, url_prefix="")


@bp.route('/iniciar_sesion', methods=('GET', 'POST'))
def iniciar_sesion():
    """Devuelve la vista de iniciar sesión.
    Inicia la sesión si los datos del formulario son correctos"""
    form = IniciarSesionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            contraseña = form.contraseña.data
            usuario = usuario_por_email_y_contraseña(email, contraseña)
            if usuario is None or not usuario.activo:
                form.email.data = ""
                flash('Usuario y/o contraseña incorrectos', 'error')
            else:
                session.clear()
                # cambiar por session['mail']?
                session['usuario'] = usuario.email
                session['id'] = usuario.id
                session['alias'] = usuario.alias
                session['es_admin'] = usuario.admin_sistema
                session['roles'] = [rol.nombre for rol in usuario.roles]
                flash('Ha iniciado sesión', 'exito')
                return redirect(url_for('home'))
        else:
            flash('No se pudo iniciar la sesión. Revise los datos ingresados',
                  'error')
    return render_template('pages/usuarios/iniciar_sesion.html', form=form)


@bp.route('/cerrar_sesion')
def cerrar_sesion():
    """Cierra la sesión activa.
    """
    del session['usuario']
    session.clear()
    flash('Se ha cerrado la sesión', 'exito')
    return redirect(url_for('home'))


@bp.route('/perfil', methods=['GET'])
@sesion_iniciada_requerida
def ver_perfil():
    """Devuelve la vista de datos del perfil 
    del usuario con sesión activa.
    """
    usuario = usuario_por_id(session.get('id'))
    return render_template("pages/usuarios/ver_usuario.html", usuario=usuario)


@bp.route('/<int:id>/editar_perfil', methods=['GET', 'POST'])
@chequear_usuario_sesion
@sesion_iniciada_requerida
def editar_perfil(id):
    """Devuelve la vista de edición de perfil del usuario
    cuyo id recibe como parámetro y edita al usuario si
    los datos del formulario son correctos.
    """
    usuario = usuario_por_id(id)
    form = UsuarioSinContraseñaForm(obj=usuario)
    if request.method == 'POST':
        if form.validate_on_submit():
            # raise Exception(f'{form.data}')
            actualizar_perfil(usuario, form.email.data, form.alias.data)
            flash(f'Se guardaron los cambios al usuario \
                Alias: {usuario.alias}, email: {usuario.email}', 'exito')
            return redirect(url_for('autenticacion.ver_perfil'))
        else:
            flash('No se pudo actualizar el registro. \
                  Revise los datos ingresados',
                  'error')
    return render_template('pages/usuarios/editar_perfil.html', form=form)
