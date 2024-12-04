from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

from src.core.oauth import oauth
from src.core.forms.autenticacion_forms import (IniciarSesionForm,
                                                CambiarContraseñaForm)
from src.core.usuarios import (actualizar_perfil, asignar_contraseña,
                               crear_solicitud, solicitud_por_email,
                               usuario_por_email, usuario_por_id,
                               usuario_por_email_y_contraseña)
from src.core.forms.usuario_forms import (UsuarioSinContraseñaForm)
from src.web.handlers.decoradores import (chequear_usuario_sesion,
                                          sesion_iniciada_requerida)

bp = Blueprint("autenticacion", __name__, url_prefix="")


def cargar_datos_sesion(id, alias, admin_sistema,
                        nombre_roles, sin_contraseña=False):
    session.clear()
    session['id'] = id
    session['alias'] = alias
    session['es_admin'] = admin_sistema
    session['roles'] = nombre_roles
    session['sin_contraseña'] = sin_contraseña


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
                nombre_roles = [rol.nombre for rol in usuario.roles]
                cargar_datos_sesion(id=usuario.id, alias=usuario.alias,
                                    admin_sistema=usuario.admin_sistema,
                                    nombre_roles=nombre_roles)
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
    del session['id']
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
    return render_template("pages/usuarios/ver_perfil.html", usuario=usuario)


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
            actualizar_perfil(usuario=usuario, email=form.email.data,
                              alias=form.alias.data)
            session['alias'] = usuario.alias
            flash(f'Se guardaron los cambios al usuario \
                Alias: {usuario.alias}, email: {usuario.email}', 'exito')
            return redirect(url_for('autenticacion.ver_perfil'))
        else:
            flash('No se pudo actualizar el registro. \
                  Revise los datos ingresados',
                  'error')
    return render_template('pages/usuarios/editar_perfil.html', form=form)


@bp.route('/cambiar_contraseña', methods=('GET', 'POST'))
@sesion_iniciada_requerida
def cambiar_contraseña():
    """Devuelve la vista que permite al usuario
    cambiar su contraseña.
    """
    if session.get('sin_contraseña'):
        flash('No tiene contraseña en el sistema \
                  para ser modificada.', 'error')
        return redirect(url_for('home'))
    else:
        usuario = usuario_por_id(session.get('id'))
        form = CambiarContraseñaForm(usuario.contraseña)
        if request.method == 'POST':
            if form.validate_on_submit():
                contraseña_nueva = form.contraseña_nueva.data
                asignar_contraseña(usuario, contraseña_nueva)
                flash('Se ha modificado la contraseña', 'exito')
                return redirect(url_for('home'))
            else:
                flash('No se pudo realizar la operación. \
                    Revise los datos ingresados.', 'error')
    return render_template('pages/usuarios/cambiar_contraseña.html', form=form)


@bp.route('/iniciar_sesion/google', methods=['GET'])
def iniciar_sesion_google():
    uri_redireccion = url_for('autenticacion.iniciar_sesion_autorizar',
                              _external=True)
    return oauth.google.authorize_redirect(uri_redireccion)


@bp.route('/iniciar_sesion/autorizar', methods=['GET'])
def iniciar_sesion_autorizar():
    """Verifica los datos obtenidos de la conexión con Google.
    Inicia sesión en caso de existir el usuario con el mail obtenido.
    Crea una solicitud pendiente de aprobación en caso de no existir.
    """
    token = oauth.google.authorize_access_token()
    info_usuario_google = token['userinfo']
    if info_usuario_google:
        email_google = info_usuario_google.get('email')
        usuario = usuario_por_email(info_usuario_google.get('email'))
        if usuario is None and info_usuario_google.get('email_verified'):
            if solicitud_por_email(email_google) is None:
                crear_solicitud(email_google)
                flash(f'Se generó la solicitud de registro del \
                        mail {email_google}. Debe ser aceptada por \
                        la administración para poder ingresar.',
                      'info')
                return redirect(url_for('home'))
            else:
                flash(f'La solicitud de registro del \
                        mail {email_google} ya existe. Debe ser aceptada por \
                        la administración para poder ingresar.',
                      'warning')
        elif not info_usuario_google.get('email_verified'):
            flash('No se pudo registrar la solicitud: email no verificado.',
                  'error')
        elif usuario.contraseña is not None:
            flash('Utilice su contraseña para ingresar al sistema.',
                  'error')
        else:
            if not usuario.activo:
                flash('No se puede iniciar la sesión. \
                       Consulte con la administración.', 'error')
            else:
                nombre_roles = [rol.nombre for rol in usuario.roles]
                cargar_datos_sesion(id=usuario.id, alias=usuario.alias,
                                    admin_sistema=usuario.admin_sistema,
                                    nombre_roles=nombre_roles, sin_contraseña=True)
                flash('Ha iniciado sesión', 'exito')
                return redirect(url_for('home'))
    return redirect(url_for('home'))

