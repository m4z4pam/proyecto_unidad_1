from conexion import conectar_bd

def obtener_proveedores():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id_proveedor, nombre, rfc, telefono, email, direccion, creado_en
        FROM proveedores
        ORDER BY nombre ASC
    """)
    proveedores = cursor.fetchall()
    conexion.close()
    return proveedores


def obtener_proveedor(id_proveedor):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id_proveedor, nombre, rfc, telefono, email, direccion, creado_en
        FROM proveedores
        WHERE id_proveedor = %s
    """, (id_proveedor,))
    proveedor = cursor.fetchone()
    conexion.close()
    return proveedor

def crear_proveedor(nombre, rfc, telefono, email, direccion):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            INSERT INTO proveedores (nombre, rfc, telefono, email, direccion)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, rfc, telefono, email, direccion))
        conexion.commit()
        return True
    except Exception as e:
        conexion.rollback()
        print("Error al crear proveedor:", e)
        return False
    finally:
        conexion.close()




def actualizar_proveedor(id_proveedor, nombre, rfc, telefono, email, direccion):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            UPDATE proveedores
            SET nombre=%s,
                rfc=%s,
                telefono=%s,
                email=%s,
                direccion=%s
            WHERE id_proveedor=%s
        """, (nombre, rfc, telefono, email, direccion, id_proveedor))
        conexion.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conexion.rollback()
        print("Error al actualizar proveedor:", e)
        return False
    finally:
        conexion.close()



def eliminar_proveedor(id_proveedor):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM proveedores WHERE id_proveedor = %s", (id_proveedor,))
        conexion.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conexion.rollback()
        print("Error al eliminar proveedor:", e)
        return False
    finally:
        conexion.close()
