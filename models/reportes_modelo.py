import io
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from conexion import conectar_bd

def reporte_ventas_pdf():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    # Obtener ventas por producto
    cursor.execute("""
        SELECT p.nombre, SUM(vd.cantidad) 
        FROM ventas_detalle vd
        JOIN productos p ON p.id_producto = vd.id_producto
        GROUP BY p.id_producto
        ORDER BY SUM(vd.cantidad) DESC
        LIMIT 10
    """)
    datos = cursor.fetchall()
    conexion.close()
    
    productos = [d[0] for d in datos]
    cantidades = [d[1] for d in datos]

    # Generar grafica con matplotlib
    plt.figure(figsize=(8,4))
    plt.barh(productos, cantidades, color='skyblue')
    plt.xlabel('Cantidad Vendida')
    plt.title('Top 10 Productos Mas Vendidos')
    
    grafica_io = io.BytesIO()
    plt.savefig(grafica_io, format='PNG', bbox_inches='tight')
    plt.close()
    grafica_io.seek(0)
    
    # Generar PDF
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("Reporte de Ventas")
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(150, 750, "Reporte de Ventas - Top 10 Productos")
    
    # Insertar la grafica
    imagen = ImageReader(grafica_io)
    pdf.drawImage(imagen, 50, 400, width=500, height=300)
    
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer
