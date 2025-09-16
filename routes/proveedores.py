from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.proveedores_modelo import (
    obtener_proveedores, obtener_proveedor, crear_proveedor,
    actualizar_proveedor, eliminar_proveedor
)  
from forms import ProveedorForm

proveedores_bp = Blueprint('proveedores', __name__, url_prefix="/proveedores")

@proveedores_bp.route("/proveedores")
def lista_proveedores():
    proveedores = obtener_proveedores()
    return render_template("proveedores_list.html", proveedores=proveedores)





@proveedores_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        telefono = form.telefono.data
        email = form.email.data
        direccion = form.direccion.data
        rfc = form.rfc.data

        if crear_proveedor(nombre, rfc, telefono, email, direccion):
            flash("Proveedor creado con exito", "success")
            return redirect(url_for("proveedores.lista_proveedores"))
        else:
            flash("Error al crear proveedor", "danger")

    return render_template("proveedores_form.html", form=form, action="Nuevo")




@proveedores_bp.route("/editar/<int:id_proveedor>", methods=["GET", "POST"])
def editar_proveedor(id_proveedor):
    proveedor = obtener_proveedor(id_proveedor)
    if not proveedor:
        flash("Proveedor no encontrado", "danger")
        return redirect(url_for("proveedores.lista_proveedores"))

    form = ProveedorForm()

    # Cuando sea un GET, rellenamos los campos manualmente
    if request.method == "GET":
        form.nombre.data = proveedor[1]     # suponiendo proveedor[1] = nombre
        form.rfc.data = proveedor[2]        # proveedor[2] = rfc
        form.telefono.data = proveedor[3]   # proveedor[3] = telefono
        form.email.data = proveedor[4]      # proveedor[4] = email
        form.direccion.data = proveedor[5]  # proveedor[5] = direccion

    if form.validate_on_submit():
        actualizado = actualizar_proveedor(
            id_proveedor,
            form.nombre.data,
            form.rfc.data,
            form.telefono.data,
            form.email.data,
            form.direccion.data,
        )
        if actualizado:
            flash("Proveedor actualizado con exito", "success")
            return redirect(url_for("proveedores.lista_proveedores"))
        else:
            flash("Error al actualizar proveedor", "danger")

    return render_template("proveedores_editar.html", form=form, proveedor=proveedor)





@proveedores_bp.route("/eliminar/<int:id_proveedor>", methods=["POST"])
def eliminar_proveedor_route(id_proveedor):
    if eliminar_proveedor(id_proveedor):
        flash("Proveedor eliminado con exito", "success")
    else:
        flash("Error al eliminar proveedor", "danger")
    return redirect(url_for("proveedores.lista_proveedores"))