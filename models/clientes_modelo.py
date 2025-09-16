from conexion import conectar_bd

def obtener_clientes():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM clientes;")
    return cursor.fetchall()

def obtener_cliente(id):  
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id_cliente=%s;", (id,))
    return cursor.fetchone()

def agregar_cliente(nombre, telefono, email, descuento=0):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO clientes (nombre, telefono, email) VALUES (%s, %s, %s);",
        (nombre, telefono, email)
    )
    conexion.commit()

def actualizar_cliente(id, nombre, telefono, email):  
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE clientes SET nombre=%s, telefono=%s, email=%s WHERE id_cliente=%s;",
        (nombre, telefono, email, id)
    )
    conexion.commit()

def eliminar_clientes(id):  
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM clientes WHERE id_cliente=%s;", (id,))
    conexion.commit()