from flask import Blueprint, render_template, request, redirect, url_for, flash, session, flash
from models.usuarios_modelo import (
    obtener_usuarios, 
    obtener_usuario, 
    crear_usuario, 
    actualizar_usuario, 
    eliminar_usuario,
    cambiar_password_usuario,
    autenticar_usuario,
    obtener_usuario_por_username,
    limpiar_usuarios_inactivos
)
from forms import UsuarioForm, EditarUsuarioForm, CambiarPasswordForm, LoginSimpleForm

usuarios_bp = Blueprint('usuarios', __name__)

# Funcion helper para verificar si esta logueado
def requiere_login():
    if 'user_id' not in session:
        flash("Debe iniciar sesion", "warning")
        return redirect(url_for('login'))
    return None

# Funcion helper para verificar si es admin
def requiere_admin():
    if 'user_id' not in session:
        flash("Debe iniciar sesion", "warning")
        return redirect(url_for('login'))
    if session.get('rol') != 'admin':
        flash("No tiene permisos de administrador", "danger")
        return redirect(url_for('index'))
    return None








# ========== RUTAS CRUD ==========

@usuarios_bp.route("/usuarios")
def lista_usuarios():
    redirect_response = requiere_admin()
    if redirect_response:
        return redirect_response
    
    usuarios = obtener_usuarios()
    return render_template("usuarios_list.html", usuarios=usuarios)


@usuarios_bp.route("/usuario/nuevo", methods=["GET", "POST"])
def nuevo_usuario():
    redirect_response = requiere_admin()
    if redirect_response:
        return redirect_response
    
    form = UsuarioForm()
    if form.validate_on_submit():
        # Verificar que el username no exista
        usuario_existente = obtener_usuario_por_username(form.username.data)
        if usuario_existente:
            flash("El nombre de usuario ya existe", "danger")
            return render_template("usuario_form.html", form=form, titulo="Nuevo Usuario")
        
        id_usuario = crear_usuario(
            form.username.data,
            form.email.data,
            form.password.data,
            form.nombre.data,
            form.apellido.data,
            form.rol.data
        )
        
        if id_usuario:
            flash("Usuario creado correctamente", "success")
            return redirect(url_for("usuarios.lista_usuarios"))
        else:
            flash("Error al crear usuario", "danger")
    
    return render_template("usr_components/usuario_form.html", form=form, titulo="Nuevo Usuario")









###
###
###

@usuarios_bp.route("/usuario/editar/<int:id_usuario>", methods=["GET", "POST"])
def editar_usuario(id_usuario):
    redirect_response = requiere_admin()
    if redirect_response:
        return redirect_response
    
    usuario = obtener_usuario(id_usuario)
    if not usuario:
        flash("Usuario no encontrado", "danger")
        return redirect(url_for("usuarios.lista_usuarios"))
    
    form = EditarUsuarioForm()
    
    if form.validate_on_submit():
        flash(f"Formulario validado. Datos: {form.data}")  
        
        # Verificar que el username no este en uso por otro usuario
        usuario_existente = obtener_usuario_por_username(form.username.data)
        if usuario_existente and usuario_existente[0] != id_usuario:
            flash("El nombre de usuario ya esta en uso", "danger")
            return render_template("usr_components/editar_usuario.html", 
                                 form=form, titulo="Editar Usuario", usuario=usuario)
        
        # Intentar actualizar el usuario
        resultado = actualizar_usuario(
            id_usuario,
            form.username.data,
            form.email.data,
            form.nombre.data,
            form.apellido.data,
            form.rol.data,
            form.activo.data
        )
        
        if resultado:
            flash("Usuario actualizado correctamente", "success")
            return redirect(url_for("usuarios.lista_usuarios"))
        else:
            flash("Error al actualizar usuario", "danger")
            flash(f"Error al actualizar usuario con ID: {id_usuario}")
    else:
        # Si el formulario no es valido, mostrar errores
        if request.method == "POST":
            flash(f"Errores de validacion: {form.errors}")
            flash("Por favor corrige los errores en el formulario", "warning")
    
    # Pre-llenar el formulario con los datos existentes
    if request.method == "GET":
        form.username.data = usuario[1]
        form.email.data = usuario[2]
        form.nombre.data = usuario[3]
        form.apellido.data = usuario[4]
        form.rol.data = usuario[5]
        form.activo.data = usuario[6]
    
    return render_template("usr_components/editar_usuario.html", 
                         form=form, titulo="Editar Usuario", usuario=usuario)
###
###
###
###




@usuarios_bp.route("/usuario/eliminar/<int:id_usuario>", methods=["GET", "POST"])
def eliminar_usuario_route(id_usuario):
    redirect_response = requiere_admin()
    if redirect_response:
        return redirect_response
    
    # No permitir que se elimine a si mismo
    if session.get('user_id') == id_usuario:
        flash("No puede eliminarse a si mismo", "warning")
        return redirect(url_for("usuarios.lista_usuarios"))
    
    if eliminar_usuario(id_usuario):
        flash("Usuario desactivado correctamente", "success")
    else:
        flash("Error al eliminar usuario", "danger")
    
    return redirect(url_for("usuarios.lista_usuarios"))



@usuarios_bp.route("/usuarios/limpiar_inactivos", methods=["POST"])
def limpiar_inactivos():
    redirect_response = requiere_admin()
    if redirect_response:
        return redirect_response

    eliminados = limpiar_usuarios_inactivos(dias=0)
    flash(f"Se eliminaron {eliminados} usuarios inactivos.", "success")
    return redirect(url_for("usuarios.lista_usuarios"))






@usuarios_bp.route("/usuario/cambiar-password/<int:id_usuario>", methods=["GET", "POST"])
def cambiar_password(id_usuario):
    redirect_response = requiere_admin()
    if redirect_response:
        return redirect_response
    
    usuario = obtener_usuario(id_usuario)
    if not usuario:
        flash("Usuario no encontrado", "danger")
        return redirect(url_for("usuarios.lista_usuarios"))
    
    form = CambiarPasswordForm()
    if form.validate_on_submit():
        if cambiar_password_usuario(id_usuario, form.nueva_password.data):
            flash("Contraseña cambiada correctamente", "success")
            return redirect(url_for("usuarios.lista_usuarios"))
        else:
            flash("Error al cambiar contraseña", "danger")
    
    return render_template("usr_components/cambiar_password.html", form=form, usuario=usuario)