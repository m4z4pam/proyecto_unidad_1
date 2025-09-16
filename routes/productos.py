from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
import io
from conexion import conectar_bd
from models.productos_modelo import (
    obtener_producto,
    obtener_productos,
    agregar_producto,
    editar_producto,
    obtener_productos_por_categoria,
    buscar_productos_por_nombre,
    obtener_productos_bajo_stock,
    eliminar_producto
)
from forms import ProductoForm as producto_form

productos_bp = Blueprint('productos', __name__)

@productos_bp.route("/productos")
def lista_productos():
    productos = obtener_productos()
    return render_template("productos_list.html", productos=productos)

@productos_bp.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():
    categorias = ["Escolares", "Oficina", "Arte"] 
    form = producto_form()
    form.categoria.choices = [(c, c) for c in categorias] 

    if form.validate_on_submit():
        agregar_producto(
            form.nombre.data,
            form.categoria.data,
            float(form.precio.data),
            int(form.stock.data),
            float(form.costo.data)
        )
        flash("Producto agregado con exito", "success")
        return redirect(url_for("productos.lista_productos"))

    return render_template("producto_form.html", form=form)

@productos_bp.route("/productos/editar/<int:id>", methods=["GET", "POST"])
def editar_producto_route(id):
    producto = obtener_producto(id)   
    if not producto:
        flash("Producto no encontrado", "error")
        return redirect(url_for("productos.lista_productos"))

    form = producto_form()

    # Cargar categorias
    form.categoria.choices = [("Escolares", "Escolares"), ("Oficina", "Oficina"), ("Arte", "Arte")]

    if request.method == "GET":
        # Prellenar el formulario con los valores actuales
        form.nombre.data = producto[1]
        form.categoria.data = producto[2]
        form.precio.data = producto[3]
        form.stock.data = producto[4]
        form.costo.data = producto[5]

    if form.validate_on_submit():
        editar_producto(id, form.nombre.data, form.categoria.data, form.precio.data, form.stock.data, form.costo.data)
        flash("Producto actualizado con exito", "success")
        return redirect(url_for("productos.lista_productos"))

    return render_template("editar_producto.html", form=form, producto=producto)


@productos_bp.route("/productos/<int:id>/eliminar", methods=["POST"])
def eliminar_producto_ruta(id):
    if request.method == "POST":
        eliminar_producto(id)
        flash("Producto desactivado con exito", "success")
        return redirect(url_for("productos.lista_productos"))
    


@productos_bp.route("/productos/categoria/<categoria>")
def productos_por_categoria(categoria):
    productos = obtener_productos_por_categoria(categoria)
    return render_template("productos_list.html", productos=productos, categoria_filtro=categoria)

@productos_bp.route("/productos/buscar")
def buscar_productos():
    nombre = request.args.get('q', '')
    if nombre:
        productos = buscar_productos_por_nombre(nombre)
    else:
        productos = obtener_productos()
    
    return render_template("productos_list.html", productos=productos, busqueda=nombre)



@productos_bp.route("/productos/stock-bajo")
def productos_stock_bajo():
    limite = request.args.get('limite', 10, type=int)
    
    # seguridad: forzar el rango entre 1 y 50
    if limite < 1:
        limite = 1
    elif limite > 50:
        limite = 50

    productos = obtener_productos_bajo_stock(limite)
    return render_template("productos_list.html", productos=productos, stock_bajo=True, limite=limite)



@productos_bp.route("/productos/inventario")
def reporte_inventario():
    productos = obtener_productos()
    productos_bajo_stock = obtener_productos_bajo_stock(limite=10)
    
    # Calcular estadisticas
    total_productos = len(productos)
    valor_total_inventario = sum(float(p[3]) * p[4] for p in productos)  # precio * stock
    productos_sin_stock = len([p for p in productos if p[4] == 0])
    
    estadisticas = {
        'total_productos': total_productos,
        'valor_total': valor_total_inventario,
        'sin_stock': productos_sin_stock,
        'bajo_stock': len(productos_bajo_stock)
    }
    
    return render_template("inventario.html", 
                         productos=productos, 
                         productos_bajo_stock=productos_bajo_stock,
                         estadisticas=estadisticas)




@productos_bp.route("/productos/inventario/pdf")
def exportar_inventario_pdf():
    productos = obtener_productos()
    productos_bajo_stock = obtener_productos_bajo_stock(limite=10)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, title ="Reporte de Productos")
    elements = []
    styles = getSampleStyleSheet()

    # Titulo
    elements.append(Paragraph("Reporte de Inventario", styles['Title']))
    elements.append(Spacer(1, 12))

    # Estadisticas
    total = len(productos)
    valor_total = sum(float(p[3]) * p[4] for p in productos)
    sin_stock = len([p for p in productos if p[4] == 0])
    bajo_stock = len(productos_bajo_stock)

    stats = f"""
    Total de productos: {total}<br/>
    Valor total inventario: ${valor_total:.2f}<br/>
    Productos sin stock: {sin_stock}<br/>
    Productos con stock bajo (≤5): {bajo_stock}
    """
    elements.append(Paragraph(stats, styles['Normal']))
    elements.append(Spacer(1, 20))

    # Tabla de productos bajo stock
    data = [["ID", "Nombre", "Categoria", "Precio", "Stock"]]
    for p in productos_bajo_stock:
        data.append([p[0], p[1], p[2], f"${p[3]:.2f}", p[4]])

    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,1), (-1,-1), colors.beige),
    ]))
    elements.append(table)

    # Generar PDF
    doc.build(elements)

    buffer.seek(0)
    response = make_response(buffer.read())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=inventario.pdf"
    return response






@productos_bp.route("/productos/ganancias/pdf")
def exportar_ganancias_pdf():
    productos = obtener_productos()  # traer todos los activos

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, title="Reporte de Ganancias")
    elements = []
    styles = getSampleStyleSheet()

    # Titulo
    elements.append(Paragraph("Reporte de Ganancias por Producto", styles['Title']))
    elements.append(Spacer(1, 12))

    # Encabezado tabla
    data = [["ID", "Nombre", "Categoria", "Costo", "Precio Venta", "Stock", "Ganancia/U", "Ganancia Total"]]

    total_ganancia = 0

    for p in productos:
        # p = (id, nombre, categoria, precio, stock, costo) 
        costo = float(p[5]) if len(p) > 5 else 0
        precio = float(p[3])
        stock = int(p[4])

        ganancia_unidad = precio - costo
        ganancia_total = ganancia_unidad * stock
        total_ganancia += ganancia_total

        data.append([
            p[0], p[1], p[2],
            f"${costo:.2f}", f"${precio:.2f}", stock,
            f"${ganancia_unidad:.2f}", f"${ganancia_total:.2f}"
        ])

    # Agregar fila de total
    data.append(["", "", "", "", "", "", "Total", f"${total_ganancia:.2f}"])

    # Construir tabla
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,1), (-1,-1), colors.beige),
        ("BACKGROUND", (-2,-1), (-1,-1), colors.lightgrey),
    ]))
    elements.append(table)

    # Generar PDF
    doc.build(elements)

    buffer.seek(0)
    response = make_response(buffer.read())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=ganancias.pdf"
    return response









@productos_bp.route("/productos/reporte_costos")
def reporte_costos():
    conexion = conectar_bd()
    cursor = conexion.cursor()

    # 1. Costo total bodega (capital inmovilizado)
    cursor.execute("SELECT SUM(costo * stock) FROM productos WHERE activo = 1;")
    costo_total = cursor.fetchone()[0] or 0

    # 2. Valor de venta
    cursor.execute("SELECT SUM(precio * stock) FROM productos WHERE activo = 1;")
    valor_venta = cursor.fetchone()[0] or 0

    # 3. Utilidad bruta proyectada
    cursor.execute("SELECT SUM((precio - costo) * stock) FROM productos WHERE activo = 1;")
    utilidad = cursor.fetchone()[0] or 0

    # 4. Perdida por inactivos (productos dados de baja)
    cursor.execute("SELECT SUM(costo * stock) FROM productos WHERE activo = 0;")
    perdida = cursor.fetchone()[0] or 0

    # 5. Costo de oportunidad por stock (productos activos guardados sin venderse)
    # Aqui todo stock activo representa dinero inmovilizado.
    costo_oportunidad = costo_total  

    conexion.close()

    # Generar PDF en memoria
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("Reporte de Costos y Utilidad")

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 750, "Reporte de Inventario y Costos")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 700, f"Costo total en bodega: ${costo_total:,.2f}")
    pdf.drawString(100, 670, f"Valor de venta potencial: ${valor_venta:,.2f}")
    pdf.drawString(100, 640, f"Utilidad proyectada: ${utilidad:,.2f}")
    pdf.drawString(100, 610, f"Perdidas por inactivos: ${perdida:,.2f}")
    pdf.drawString(100, 580, f"Costo de oportunidad (dinero inmovilizado en stock): ${costo_oportunidad:,.2f}")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="reporte_costos.pdf",
        mimetype="application/pdf"
    )



@productos_bp.route('/productos/rotacion')
def reporte_rotacion():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    query = """
        SELECT 
            p.id_producto,
            p.nombre,
            COALESCE(SUM(vd.cantidad), 0) AS ventas_mes,
            ROUND(COALESCE(SUM(vd.cantidad), 0) / NULLIF(AVG(p.stock), 0), 2) AS rotacion
        FROM productos p
        LEFT JOIN ventas_detalle vd ON p.id_producto = vd.id_producto
        LEFT JOIN ventas v ON vd.id_venta = v.id_venta
            AND v.fecha >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        GROUP BY p.id_producto, p.nombre
        ORDER BY rotacion DESC;
    """
    
    cursor.execute(query)
    rotacion = cursor.fetchall()
    conexion.close()

    return render_template("productos_rotacion.html", rotacion=rotacion)
