import math
from flask import Blueprint, flash, redirect, render_template, request, url_for
from src.core.usuarios import actualizar_usuario, crear_usuario, listar_usuarios, roles_por_usuario, usuario_por_id
from src.core.usuarios.usuario_forms import UsuarioEditarForm, UsuarioForm
from src.core.database import db
from src.web.handlers.decoradores import (chequear_permiso,
                                            sesion_iniciada_requerida)

bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@bp.route('/', methods=['GET'])
@chequear_permiso('usuario_listar')
@sesion_iniciada_requerida
def listado_usuarios():
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "id")
    pagina = int(request.args.get("pagina", 1))
    cant_por_pagina = int(request.args.get("cant_por_pagina", 10))
    email_filtro = request.args.get("email", "")

    cant_resultados, usuarios = listar_usuarios(
        email_filtro, orden, ordenar_por, pagina, cant_por_pagina
        )

    cant_paginas = math.ceil(cant_resultados / cant_por_pagina)

    return render_template(
        "pages/usuarios/listado_usuarios.html",
        usuarios=usuarios,
        cant_resultados=cant_resultados,
        cant_paginas=cant_paginas,
        pagina=pagina,
        orden=orden,
        ordenar_por=ordenar_por,
        email_filtro=email_filtro,
    )


@bp.route('/registrar_usuario', methods=['GET', 'POST'])
@chequear_permiso('usuario_crear')
@sesion_iniciada_requerida
def registrar_usuario():
    form = UsuarioForm(request.form)
    if form.validate_on_submit():
        # raise Exception(f'{form.data}')
        usuario = crear_usuario(form.email.data, form.contraseña.data,
                                form.alias.data, form.admin_sistema.data,
                                form.roles.data)
        flash(f'Registro exitoso. \
              Alias: {usuario.alias}, email: {usuario.email}', 'exito')
        return redirect(url_for('usuarios.listado_usuarios'))
    return render_template('pages/usuarios/registrar_usuario.html', form=form)


@bp.route('/<int:id>', methods=['GET'])
@chequear_permiso('usuario_mostrar')
@sesion_iniciada_requerida
def ver_usuario(id):
    usuario = usuario_por_id(id)
    return render_template("pages/usuarios/ver_usuario.html", usuario=usuario)


@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@chequear_permiso('usuario_editar')
@sesion_iniciada_requerida
def editar_usuario(id):
    usuario = usuario_por_id(id)
    form = UsuarioEditarForm(obj=usuario)
    if request.method == 'GET':
        form.roles.data = [str(rol.id) for rol in roles_por_usuario(id)]
    elif form.validate_on_submit():
        # raise Exception(f'{form.data}')
        actualizar_usuario(usuario, form.email.data, form.alias.data, form.admin_sistema.data, form.roles.data)
        flash(f'Se guardaron los cambios al usuario \
              Alias: {usuario.alias}, email: {usuario.email}', 'exito')
        return redirect(url_for('usuarios.listado_usuarios'))
    return render_template('pages/usuarios/editar_usuario.html', form=form)


@bp.route('/<int:id>/bloquear', methods=['GET'])
@chequear_permiso('usuario_bloquear')
@sesion_iniciada_requerida
def bloquear_usuario(id):
    usuario = usuario_por_id(id)
    usuario.activo = False
    db.session.commit()
    flash(f'Se ha bloqueado al usuario \
              Alias: {usuario.alias}, email: {usuario.email}', 'exito')
    return redirect(request.referrer)


@bp.route('/<int:id>/activar', methods=['GET'])
@chequear_permiso('usuario_activar')
@sesion_iniciada_requerida
def activar_usuario(id):
    usuario = usuario_por_id(id)
    usuario.activo = True
    db.session.commit()
    flash(f'Se ha activado al usuario \
              Alias: {usuario.alias}, email: {usuario.email}', 'exito')
    return redirect(request.referrer)


@bp.route('/<int:id>/eliminar', methods=['GET'])
@chequear_permiso('usuario_eliminar')
@sesion_iniciada_requerida
def eliminar_usuario(id):
    usuario = usuario_por_id(id)
    db.session.delete(usuario)
    db.session.commit()
    flash(f'Se ha eliminado al usuario \
              Alias: {usuario.alias}, email: {usuario.alias}', 'exito')
    return redirect(url_for('usuarios.listado_usuarios'))
