from conexion import conectar_bd

def asociar_producto_proveedor(id_producto, id_proveedor):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            INSERT INTO productos_proveedores (id_producto, id_proveedor)
            VALUES (%s, %s)
        """, (id_producto, id_proveedor))
        conexion.commit()
        return True
    except Exception as e:
        conexion.rollback()
        print("Error al asociar producto con proveedor:", e)
        return False
    finally:
        conexion.close()


def obtener_proveedores_de_producto(id_producto):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            SELECT p.id_proveedor, p.nombre, p.rfc, p.telefono, p.email, p.direccion
            FROM proveedores p
            JOIN productos_proveedores pp ON p.id_proveedor = pp.id_proveedor
            WHERE pp.id_producto = %s
        """, (id_producto,))
        return cursor.fetchall()
    except Exception as e:
        print("Error al obtener proveedores del producto:", e)
        return []
    finally:
        conexion.close()


def eliminar_relacion_producto_proveedor(id_producto, id_proveedor):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            DELETE FROM productos_proveedores
            WHERE id_producto=%s AND id_proveedor=%s
        """, (id_producto, id_proveedor))
        conexion.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conexion.rollback()
        print("Error al eliminar relacion especifica:", e)
        return False
    finally:
        conexion.close()
