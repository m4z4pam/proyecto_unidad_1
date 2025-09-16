from conexion import conectar_bd

def obtener_ventas():
    """Obtiene todas las ventas con informacion del cliente"""
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT v.id_venta, v.fecha, c.nombre, v.total 
        FROM ventas v
        LEFT JOIN clientes c ON v.id_cliente = c.id_cliente
        ORDER BY v.fecha DESC
    """)
    ventas = cursor.fetchall()
    conexion.close()
    return ventas

def obtener_venta_con_detalle(id_venta):
    """Obtiene una venta especifica con todos sus detalles"""
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    # Obtener cabecera de venta
    cursor.execute("""
        SELECT v.id_venta, v.fecha, v.id_cliente, c.nombre, v.total
        FROM ventas v
        LEFT JOIN clientes c ON v.id_cliente = c.id_cliente
        WHERE v.id_venta = %s
    """, (id_venta,))
    venta = cursor.fetchone()
    
    # Obtener detalles de venta
    cursor.execute("""
        SELECT vd.id_detalle, p.nombre, vd.cantidad, vd.precio_unitario, vd.total
        FROM ventas_detalle vd
        JOIN productos p ON vd.id_producto = p.id_producto
        WHERE vd.id_venta = %s
    """, (id_venta,))
    detalles = cursor.fetchall()
    
    conexion.close()
    return venta, detalles

def crear_venta(id_cliente, productos):

    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    try:
        # Comenzar transaccion
        cursor.execute("START TRANSACTION")
        
        # Crear la venta (cabecera)
        cursor.execute("""
            INSERT INTO ventas (id_cliente, total) 
            VALUES (%s, 0)
        """, (id_cliente,))
        
        id_venta = cursor.lastrowid
        total_venta = 0
        
        #Procesar cada producto
        for id_producto, cantidad in productos:
            # Verificar stock disponible
            cursor.execute("SELECT stock, precio FROM productos WHERE id_producto = %s", (id_producto,))
            producto_info = cursor.fetchone()
            
            if not producto_info:
                raise Exception(f"Producto {id_producto} no existe")
            
            stock_actual, precio = producto_info
            
            if stock_actual < cantidad:
                raise Exception(f"Stock insuficiente para producto {id_producto}. Disponible: {stock_actual}, Solicitado: {cantidad}")
            
            # Calcular total del detalle
            total_detalle = precio * cantidad
            total_venta += total_detalle
            
            # Crear detalle de venta
            cursor.execute("""
                INSERT INTO ventas_detalle (id_venta, id_producto, cantidad, precio_unitario, total)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_venta, id_producto, cantidad, precio, total_detalle))
            
            # Actualizar stock del producto
            cursor.execute("""
                UPDATE productos 
                SET stock = stock - %s 
                WHERE id_producto = %s
            """, (cantidad, id_producto))
        
        # Actualizar total de la venta
        cursor.execute("""
            UPDATE ventas 
            SET total = %s 
            WHERE id_venta = %s
        """, (total_venta, id_venta))
        
        # Confirmar transaccion
        conexion.commit()
        conexion.close()
        return id_venta
        
    except Exception as e:
        # Revertir transaccion en caso de error
        conexion.rollback()
        conexion.close()
        raise e

def obtener_productos_disponibles():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id_producto, nombre, categoria, precio, stock 
        FROM productos 
        WHERE stock > 0
        ORDER BY categoria, nombre
    """)
    productos = cursor.fetchall()
    conexion.close()
    return productos


def eliminar_venta_bd(id_venta):
    """
    Elimina una venta y restaura el stock de productos
    """
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    try:
        cursor.execute("START TRANSACTION")
        
        # Obtener detalles para restaurar stock
        cursor.execute("""
            SELECT id_producto, cantidad
            FROM ventas_detalle 
            WHERE id_venta = %s
        """, (id_venta,))
        detalles = cursor.fetchall()
        
        # Restaurar stock de cada producto
        for id_producto, cantidad in detalles:
            cursor.execute("""
                UPDATE productos 
                SET stock = stock + %s 
                WHERE id_producto = %s
            """, (cantidad, id_producto))
        
        # Eliminar detalles
        cursor.execute("DELETE FROM ventas_detalle WHERE id_venta = %s", (id_venta,))
        
        # Eliminar venta
        cursor.execute("DELETE FROM ventas WHERE id_venta = %s", (id_venta,))
        
        conexion.commit()
        conexion.close()
        
    except Exception as e:
        conexion.rollback()
        conexion.close()
        raise e

def obtener_resumen_ventas(fecha_inicio=None, fecha_fin=None):
    """Obtiene resumen de ventas por periodo"""
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    sql_base = """
        SELECT 
            COUNT(*) as total_ventas,
            SUM(total) as total_ingresos,
            AVG(total) as promedio_venta
        FROM ventas
    """
    
    params = []
    if fecha_inicio and fecha_fin:
        sql_base += " WHERE fecha BETWEEN %s AND %s"
        params = [fecha_inicio, fecha_fin]
    elif fecha_inicio:
        sql_base += " WHERE fecha >= %s"
        params = [fecha_inicio]
    elif fecha_fin:
        sql_base += " WHERE fecha <= %s"
        params = [fecha_fin]
    
    cursor.execute(sql_base, params)
    resumen = cursor.fetchone()
    conexion.close()
    return resumen





def obtener_productos_mas_vendidos(limite=10):
    """Obtiene los productos mas vendidos"""
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT 
            p.nombre,
            p.categoria,
            SUM(vd.cantidad) as total_vendido,
            SUM(vd.total) as ingresos_producto
        FROM ventas_detalle vd
        JOIN productos p ON vd.id_producto = p.id_producto
        GROUP BY p.id_producto, p.nombre, p.categoria
        ORDER BY total_vendido DESC
        LIMIT %s
    """, (limite,))
    productos = cursor.fetchall()
    conexion.close()
    return productos





def obtener_productos_menos_vendidos(limite=10):
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        query = """
            SELECT p.id_producto, p.nombre, SUM(vd.cantidad) AS total_vendidos
            FROM ventas_detalle vd
            INNER JOIN productos p ON vd.id_producto = p.id_producto
            GROUP BY p.id_producto, p.nombre
            ORDER BY total_vendidos ASC
            LIMIT %s;
        """
        cursor.execute(query, (limite,))
        productos = cursor.fetchall()
        conexion.close()
        return productos
    except Exception as e:
        print("Error en obtener_productos_menos_vendidos:", e)
        return []





def actualizar_venta(id_venta, id_cliente, productos):

    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        # Eliminar detalles anteriores
        cursor.execute("DELETE FROM ventas_detalle WHERE id_venta = %s;", (id_venta,))
        
        # Insertar nuevos detalles
        total_venta = 0
        for id_producto, cantidad in productos:
            # Obtener precio del producto
            cursor.execute("SELECT precio FROM productos WHERE id_producto = %s;", (id_producto,))
            precio = cursor.fetchone()[0]
            total = precio * cantidad
            total_venta += total
            
            cursor.execute("""
                INSERT INTO ventas_detalle (id_venta, id_producto, cantidad, precio_unitario, total)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_venta, id_producto, cantidad, precio, total))
        
        # Actualizar cabecera de la venta
        cursor.execute("""
            UPDATE ventas
            SET id_cliente=%s, total=%s
            WHERE id_venta=%s
        """, (id_cliente, total_venta, id_venta))
        
        conexion.commit()
        return True
    except Exception as e:
        conexion.rollback()
        print(f"Error al actualizar venta: {e}")
        return False
    finally:
        conexion.close()
