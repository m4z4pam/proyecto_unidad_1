from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.productos_proveedores_modelo import (
    obtener_proveedores_de_producto,
    eliminar_relacion_producto_proveedor,
    asociar_producto_proveedor
)
from models.productos_modelo import (
    obtener_producto,
    obtener_productos
)
from models.proveedores_modelo import(
    obtener_proveedor,
    obtener_proveedores
)
from forms import AsociarProveedorForm 


productos_proveedores_bp = Blueprint('productos_proveedores', __name__)

@productos_proveedores_bp.route("/productos-proveedores")
def lista_productos_proveedores():
    productos = obtener_productos()
    return render_template("proveedores_producto_list.html", productos=productos)


@productos_proveedores_bp.route("/producto/<int:id_producto>/proveedores")
def ver_proveedores_de_producto(id_producto):
    producto = obtener_producto(id_producto)
    print("DEBUG PRODUCTO:", producto)
    proveedores = obtener_proveedores_de_producto(id_producto)
    return render_template("proveedores_producto.html",
                           producto=producto, proveedores=proveedores)





@productos_proveedores_bp.route("/asociar/<int:id_producto>", methods=["GET", "POST"])
def asociar(id_producto):
    try:
        producto = obtener_producto(id_producto)
        if not producto:
            flash("Producto no encontrado", "danger")
            return redirect(url_for("productos_proveedores.lista_productos_proveedores"))
        
        proveedores = obtener_proveedores()
        
        form = AsociarProveedorForm(proveedores=proveedores)
        
        if form.validate_on_submit():
            id_proveedor = form.id_proveedor.data
            try:
                if asociar_producto_proveedor(id_producto, id_proveedor):
                    flash("Proveedor asociado correctamente", "success")
                else:
                    flash("Error al asociar proveedor", "danger")
            except Exception as e:
                flash(f"Error al asociar proveedor: {str(e)}", "danger")
            return redirect(url_for("productos_proveedores.lista_productos_proveedores"))
        
        return render_template(
            "asociar_proveedores_producto.html",
            producto=producto,
            proveedores=proveedores,
            form=form
        )
    except Exception as e:
        flash(f"Error al cargar datos: {str(e)}", "danger")
        return redirect(url_for("productos_proveedores.lista_productos_proveedores"))


@productos_proveedores_bp.route("/relacion/eliminar/<int:id_producto>/<int:id_proveedor>", methods=["POST"])
def eliminar_relacion_pp(id_producto, id_proveedor):
    if eliminar_relacion_producto_proveedor(id_producto, id_proveedor):
        flash("Relacion producto-proveedor eliminada", "success")
    else:
        flash("Error al eliminar relacion", "danger")
    return redirect(request.referrer or url_for("index"))

    
