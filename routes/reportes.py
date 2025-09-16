from flask import Blueprint, send_file
from models.reportes_modelo import reporte_ventas_pdf

reportes_bp = Blueprint("reportes", __name__)

@reportes_bp.route("/reportes/ventas")
def ventas():
    pdf = reporte_ventas_pdf()
    return send_file(
        pdf,
        as_attachment=True,
        download_name="reporte_ventas.pdf",
        mimetype="application/pdf"
    )
