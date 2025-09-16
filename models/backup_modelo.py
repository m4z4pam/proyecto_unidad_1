import pymysql
import io
import zipfile
from conexion import conectar_bd

def backup_completo():
    conexion = conectar_bd()
    cursor = conexion.cursor()

    # Obtener todas las tablas de la BD
    cursor.execute("SHOW TABLES;")
    tablas = [t[0] for t in cursor.fetchall()]

    # Crear un buffer ZIP en memoria
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for tabla in tablas:
            cursor.execute(f"SELECT * FROM {tabla};")
            filas = cursor.fetchall()
            columnas = [i[0] for i in cursor.description]

            # Crear CSV en memoria
            csv_buffer = io.StringIO()
            csv_buffer.write(",".join(columnas) + "\n")
            for fila in filas:
                csv_buffer.write(",".join([str(x) for x in fila]) + "\n")

            # Agregar CSV al ZIP
            zip_file.writestr(f"{tabla}.csv", csv_buffer.getvalue())

    conexion.close()
    zip_buffer.seek(0)
    return zip_buffer
