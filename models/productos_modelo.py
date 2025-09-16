from conexion import conectar_bd

def obtener_productos():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE activo=1;")
    productos = cursor.fetchall()
    conexion.close()
    return productos

def obtener_producto(id):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE id_producto=%s AND activo=1;", (id,))
    producto = cursor.fetchone()
    conexion.close()
    return producto

def agregar_producto(nombre, categoria, precio, stock, costo):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, categoria, precio, stock, costo) VALUES (%s, %s, %s, %s, %s);",
        (nombre, categoria, precio, stock, costo) 
    )
    conexion.commit()
    conexion.close()


def editar_producto(id, nombre, categoria, precio, stock):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE productos SET nombre=%s, categoria=%s, precio=%s, stock=%s, costo=%s WHERE id_producto=%s;",
        (nombre, categoria, precio, stock, id)
    )
    conexion.commit()
    conexion.close()

def eliminar_producto(id):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("UPDATE productos SET activo=0 WHERE id_producto=%s;", (id,))
    conexion.commit()
    conexion.close()

def obtener_productos_por_categoria(categoria):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE categoria=%s AND activo=1 ORDER BY nombre;", (categoria,))
    productos = cursor.fetchall()
    conexion.close()
    return productos

def buscar_productos_por_nombre(nombre):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM productos WHERE nombre LIKE %s AND activo=1 ORDER BY nombre;",
        (f'%{nombre}%',)
    )
    productos = cursor.fetchall()
    conexion.close()
    return productos

def obtener_productos_bajo_stock(limite=10):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE stock <= %s ORDER BY stock ASC;", (limite,))
    productos = cursor.fetchall()
    conexion.close()
    return productos
