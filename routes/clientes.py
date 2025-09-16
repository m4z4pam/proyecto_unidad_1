from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.clientes_modelo import (
    obtener_cliente,
    obtener_clientes,
    agregar_cliente,
    actualizar_cliente,
    eliminar_clientes
)
from forms import ClienteForm

clientes_bp = Blueprint("clientes", __name__)

@clientes_bp.route("/clientes")
def lista_clientes():
    clientes = obtener_clientes()
    return render_template("clientes_list.html", clientes=clientes)

@clientes_bp.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():
    form = ClienteForm()
    if form.validate_on_submit(): 
        agregar_cliente(
            form.nombre.data, 
            form.telefono.data, 
            form.email.data
        )
        flash("Cliente agregado con exito", "success")
        return redirect(url_for("clientes.lista_clientes"))
    return render_template("cliente_form.html", form=form)



@clientes_bp.route("/clientes/<int:id>/editar", methods=["GET", "POST"])
def editar_cliente(id):
    cliente = obtener_cliente(id)
    if not cliente:
        flash("Cliente no encontrado", "danger")
        return redirect(url_for("clientes.lista_clientes"))

    form = ClienteForm()

    if request.method == "GET":
        form.nombre.data = cliente[1]
        form.telefono.data = cliente[2]
        form.email.data = cliente[3]

    if form.validate_on_submit():
        actualizar_cliente(id, form.nombre.data, form.telefono.data, form.email.data)
        flash("Cliente actualizado correctamente", "success")
        return redirect(url_for("clientes.lista_clientes"))

    return render_template("editar_cliente.html", form=form, cliente=cliente)






@clientes_bp.route("/clientes/<int:id>/eliminar", methods=["GET", "POST"])
def eliminar_cliente(id):
    if request.method == "POST":
        eliminar_clientes(id)
        flash("Cliente eliminado con exito", "success")
        return redirect(url_for("clientes.lista_clientes"))
    
