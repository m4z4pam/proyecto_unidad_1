from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import ventas_modelo
from models import clientes_modelo 
from forms import NuevaVentaForm



ventas_bp = Blueprint('ventas', __name__)

@ventas_bp.route('/ventas')
def listar_ventas():
    ventas = ventas_modelo.obtener_ventas()
    return render_template('ventas_list.html', ventas=ventas)

@ventas_bp.route('/ventas/nueva', methods=['GET', 'POST'])
def nueva_venta():
    form = NuevaVentaForm()

    clientes = clientes_modelo.obtener_clientes()
    form.id_cliente.choices = [(c[0], c[1]) for c in clientes]

    productos = ventas_modelo.obtener_productos_disponibles()

    if form.validate_on_submit():
        id_cliente = form.id_cliente.data
        productos_seleccionados = []

        for key, value in request.form.items():
            if key.startswith("producto_") and value:
                cantidad = int(value)
                if cantidad > 0:
                    id_producto = int(key.split("_")[1])
                    productos_seleccionados.append((id_producto, cantidad))

        if not productos_seleccionados:
            flash("Debes seleccionar al menos un producto con cantidad mayor a 0", "danger")
            return redirect(url_for("ventas.nueva_venta"))

        try:
            id_venta = ventas_modelo.crear_venta(id_cliente, productos_seleccionados)
            flash(f"Venta #{id_venta} creada exitosamente", "success")
            return redirect(url_for("ventas.listar_ventas"))
        except Exception as e:
            flash(f"Error al crear la venta: {e}", "danger")
            return redirect(url_for("ventas.nueva_venta"))

    return render_template("ventas_form.html", form=form, clientes=clientes, productos=productos)



@ventas_bp.route('/ventas/<int:id_venta>')
def ver_venta(id_venta):
    try:
        venta, detalles = ventas_modelo.obtener_venta_con_detalle(id_venta)
        if not venta:
            flash(" La venta no existe", "warning")
            return redirect(url_for("ventas.listar_ventas"))
        
        return render_template("venta_detalle.html", venta=venta, detalles=detalles)
    except Exception as e:
        flash(f" Error al cargar la venta: {e}", "danger")
        return redirect(url_for("ventas.listar_ventas"))


@ventas_bp.route('/eliminar/<int:id_venta>', methods=['POST', 'GET'])
def eliminar_venta_route(id_venta):
    try:
        ventas_modelo.eliminar_venta_bd(id_venta) 
        flash("Venta eliminada correctamente ", "success")
    except Exception as e:
        flash(f"Error al eliminar venta: {str(e)}", "danger")
    
    return redirect(url_for('ventas.listar_ventas'))



@ventas_bp.route('/ventas/resumen', methods=['GET', 'POST'])
def resumen_ventas():
    fecha_inicio = None
    fecha_fin = None

    if request.method == 'POST':
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
    else:
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')

    resumen = ventas_modelo.obtener_resumen_ventas(fecha_inicio, fecha_fin)

    return render_template("ventas_resumen.html", 
                           resumen=resumen,
                           fecha_inicio=fecha_inicio,
                           fecha_fin=fecha_fin)



@ventas_bp.route('/ventas/top-productos', methods=['GET'])
def top_productos():
    try:
        limite = request.args.get('limite', default=10, type=int) 
        productos = ventas_modelo.obtener_productos_mas_vendidos(limite)

        if not productos:
            productos = []

        return render_template(
            "ventas_top_productos.html",
            productos=productos,
            limite=limite
        )
    except Exception as e:
        flash(f"Error al obtener productos mas vendidos: {str(e)}", "danger")
        return redirect(url_for('ventas.listar_ventas'))



@ventas_bp.route('/ventas/menos-productos', methods=['GET'])
def menos_productos():
    try:
        limite = request.args.get('limite', default=10, type=int) 
        productos = ventas_modelo.obtener_productos_menos_vendidos(limite)

        if not productos:
            productos = []

        return render_template(
            "ventas_menos_productos.html",
            productos=productos,
            limite=limite
        )
    except Exception as e:
        flash(f"Error al obtener productos menos vendidos: {str(e)}", "danger")
        return redirect(url_for('ventas.listar_ventas'))





@ventas_bp.route('/ventas/editar/<int:id_venta>', methods=['GET', 'POST'])
def editar_venta(id_venta):

    venta, detalles = ventas_modelo.obtener_venta_con_detalle(id_venta)
    if not venta:
        flash("Venta no encontrada", "danger")
        return redirect(url_for("ventas.listar_ventas"))

    if request.method == 'POST':
        id_cliente = request.form.get("id_cliente")
        productos = []

        for key, value in request.form.items():
            if key.startswith("producto_") and value:
                id_producto = key.split("_")[1]
                cantidad = int(value)
                if cantidad > 0:
                    productos.append((id_producto, cantidad))

        if not id_cliente:
            flash("Debes seleccionar un cliente", "danger")
            return redirect(url_for("ventas.editar_venta", id_venta=id_venta))

        if not productos:
            flash("Debes seleccionar al menos un producto con cantidad mayor a 0", "danger")
            return redirect(url_for("ventas.editar_venta", id_venta=id_venta))

        try:
            if ventas_modelo.actualizar_venta(id_venta, id_cliente, productos):
                flash("Venta actualizada con exito", "success")
            else:
                flash("Error al actualizar la venta", "danger")
            return redirect(url_for("ventas.listar_ventas"))
        except Exception as e:
            flash(f"Error al actualizar: {e}", "danger")
            return redirect(url_for("ventas.editar_venta", id_venta=id_venta))

 
    clientes = clientes_modelo.obtener_clientes()
    productos = ventas_modelo.obtener_productos_disponibles()

   
    cantidades_existentes = {str(d[0]): d[2] for d in detalles}  
    

    return render_template(
        "venta_editar.html",
        clientes=clientes,
        productos=productos,
        venta=venta,
        cantidades_existentes=cantidades_existentes,
        modo_edicion=True
    )
