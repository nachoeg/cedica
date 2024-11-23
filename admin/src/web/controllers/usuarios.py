import math

from flask import (Blueprint, current_app, flash, redirect,
                   render_template, request, url_for)

from src.core.usuarios import (actualizar_perfil, actualizar_usuario,
                               crear_usuario, listar_usuarios, nombres_roles,
                               roles_por_usuario, usuario_por_id)
from src.core.forms.usuario_forms import UsuarioSinContraseñaForm, UsuarioForm
from src.core.database import db
from src.web.handlers.decoradores import (no_modificar_admin, chequear_permiso,
                                          sesion_iniciada_requerida)
from src.web.handlers.funciones_auxiliares import (palabra_a_booleano,
                                                   convertir_a_entero)

bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@bp.route('/', methods=['GET'])
@chequear_permiso('usuario_listar')
@sesion_iniciada_requerida
def listado_usuarios():
    """Devuelve la vista de usuarios en la base de datos
    Los datos se envían paginados, filtrados y ordenados.
    """
    cant_filas = current_app.config.get("TABLA_CANT_FILAS")

    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "id")
    pagina = convertir_a_entero(request.args.get("pagina", 1))
    cant_por_pagina = int(request.args.get("cant_por_pagina", cant_filas))
    email_filtro = request.args.get("email", "")
    activo_filtro = request.args.get("activo", "")
    rol_filtro = request.args.get("rol", "")

    # activo_filtro = palabra_a_booleano(activo_filtro)
    cant_resultados, usuarios = listar_usuarios(
        orden, ordenar_por, pagina, cant_por_pagina,
        email_filtro, palabra_a_booleano(activo_filtro), rol_filtro
        )

    cant_paginas = math.ceil(cant_resultados / cant_por_pagina)

    roles = nombres_roles()
    roles.append('Sin rol')

    return render_template("pages/usuarios/listado_usuarios.html",
                           usuarios=usuarios,
                           cant_resultados=cant_resultados,
                           cant_paginas=cant_paginas,
                           pagina=pagina,
                           orden=orden,
                           ordenar_por=ordenar_por,
                           email_filtro=email_filtro,
                           activo_filtro=activo_filtro,
                           rol_filtro=rol_filtro,
                           roles=roles
                           )


@bp.route('/registrar_usuario', methods=['GET', 'POST'])
@chequear_permiso('usuario_crear')
@sesion_iniciada_requerida
def registrar_usuario():
    """Devuelve la vista que permite registrar un usuario.
    Registra al usuario si los datos del formulario son correctos.
    """
    form = UsuarioForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            usuario = crear_usuario(email=form.email.data,
                                    contraseña=form.contraseña.data,
                                    alias=form.alias.data,
                                    admin_sistema=form.admin_sistema.data,
                                    id_roles=form.roles.data)
            flash(f'Registro exitoso. \
                Alias: {usuario.alias}, email: {usuario.email}', 'exito')
            return redirect(url_for('usuarios.listado_usuarios'))
        else:
            flash('No se pudo generar el registro. \
                  Revise los datos ingresados',
                  'error')
    return render_template('pages/usuarios/registrar_usuario.html', form=form)


@bp.route('/<int:id>', methods=['GET'])
@chequear_permiso('usuario_mostrar')
@sesion_iniciada_requerida
def ver_usuario(id):
    """Devuelve la vista de los datos del usuario
    cuyo id recibe como parámetro.
    """
    usuario = usuario_por_id(id)
    return render_template("pages/usuarios/ver_usuario.html", usuario=usuario)


@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@chequear_permiso('usuario_editar')
@sesion_iniciada_requerida
def editar_usuario(id):
    """Devuelve la vista de edición de perfil del usuario
    cuyo id recibe como parámetro y edita al usuario si
    los datos del formulario son correctos.
    """
    usuario = usuario_por_id(id)
    form = UsuarioSinContraseñaForm(obj=usuario)
    if request.method == 'GET':
        form.roles.data = [rol.id for rol in roles_por_usuario(id)]
    if request.method == 'POST':
        if form.validate_on_submit():
            if usuario.admin_sistema:
                actualizar_perfil(usuario=usuario, email=form.email.data,
                                  alias=form.alias.data)
            else:
                actualizar_usuario(usuario=usuario, email=form.email.data,
                                   alias=form.alias.data,
                                   admin_sistema=form.admin_sistema.data,
                                   id_roles=form.roles.data)
            flash(f'Se guardaron los cambios al usuario \
                Alias: {usuario.alias}, email: {usuario.email}', 'exito')
            return redirect(url_for('usuarios.listado_usuarios'))
        else:
            flash('No se pudo actualizar el registro. \
                  Revise los datos ingresados',
                  'error')
    return render_template('pages/usuarios/editar_usuario.html',
                           form=form, usuario=usuario)


@bp.route('/<int:id>/bloquear', methods=['GET'])
@chequear_permiso('usuario_bloquear')
@no_modificar_admin
@sesion_iniciada_requerida
def bloquear_usuario(id):
    usuario = usuario_por_id(id)
    if usuario.activo:
        usuario.activo = False
        db.session.commit()
        flash(f'Se ha bloqueado al usuario \
                Alias: {usuario.alias}, email: {usuario.email}', 'exito')
    else:
        flash(f'El usuario \
                Alias: {usuario.alias}, email: {usuario.email} \
                ya se encuentra bloqueado', 'info')
    return redirect(url_for('usuarios.listado_usuarios'))


@bp.route('/<int:id>/activar', methods=['GET'])
@chequear_permiso('usuario_activar')
@sesion_iniciada_requerida
def activar_usuario(id):
    usuario = usuario_por_id(id)
    if not usuario.activo:
        usuario.activo = True
        db.session.commit()
        flash(f'Se ha activado al usuario \
                Alias: {usuario.alias}, email: {usuario.email}', 'exito')
    else:
        flash(f'El usuario \
                Alias: {usuario.alias}, email: {usuario.email} \
                ya se encuentra activo', 'info')
    return redirect(url_for('usuarios.listado_usuarios'))


@bp.route('/<int:id>/eliminar', methods=['GET'])
@chequear_permiso('usuario_eliminar')
@no_modificar_admin
@sesion_iniciada_requerida
def eliminar_usuario(id):
    usuario = usuario_por_id(id)
    db.session.delete(usuario)
    db.session.commit()
    flash(f'Se ha eliminado al usuario \
            Alias: {usuario.alias}, email: {usuario.alias}', 'exito')
    return redirect(url_for('usuarios.listado_usuarios'))
