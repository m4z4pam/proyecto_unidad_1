from flask import Blueprint, send_file
from models.backup_modelo import backup_completo
import io

backup_bp = Blueprint('backup', __name__)

@backup_bp.route("/backup/total", methods=["GET"])
def backup_total():
    try:
        zip_buffer = backup_completo()
        return send_file(
            zip_buffer,
            as_attachment=True,
            download_name="backup_completo.zip",
            mimetype="application/zip"
        )
    except Exception as e:
        return f"Error al generar backup: {str(e)}"
