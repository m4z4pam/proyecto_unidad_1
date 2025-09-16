import bcrypt
from datetime import datetime
from conexion import conectar_bd
from flask import flash

def hash_password(password):
    """Hashea una contraseña usando bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verificar_password(password, hashed):
    """Verifica si una contraseña coincide con el hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))







# ========== CRUD BaSICO ==========






def obtener_usuarios():
    """Obtiene todos los usuarios activos"""
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            SELECT id_usuario, username, email, nombre, apellido, rol, activo, fecha_creacion, ultimo_login
            FROM usuarios 
            ORDER BY fecha_creacion DESC
        """)
        return cursor.fetchall()
    except Exception as e:
        print("Error al obtener usuarios:", e)
        return []
    finally:
        conexion.close()

def obtener_usuario(id_usuario):
    """Obtiene un usuario por su ID"""
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            SELECT id_usuario, username, email, nombre, apellido, rol, activo, fecha_creacion, ultimo_login
            FROM usuarios 
            WHERE id_usuario = %s
        """, (id_usuario,))
        return cursor.fetchone()
    except Exception as e:
        print("Error al obtener usuario:", e)
        return None
    finally:
        conexion.close()

def crear_usuario(username, email, password, nombre, apellido=None, rol='usuario'):
    """Crea un nuevo usuario"""
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        password_hash = hash_password(password)
        cursor.execute("""
            INSERT INTO usuarios (username, email, password_hash, nombre, apellido, rol)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, email, password_hash, nombre, apellido, rol))
        conexion.commit()
        return cursor.lastrowid
    except Exception as e:
        print("Error al crear usuario:", e)
        return None
    finally:
        conexion.close()


def actualizar_usuario(id_usuario, username, email, nombre, apellido, rol, activo=True):
    """Actualiza un usuario existente (sin cambiar contraseña)"""
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        flash(f"Actualizando usuario {id_usuario} con datos:")
        flash(f"Username: {username}, Email: {email}, Nombre: {nombre}")
        flash(f"Apellido: {apellido}, Rol: {rol}, Activo: {activo}") 
        
        cursor.execute("""
            UPDATE usuarios 
            SET username = %s, email = %s, nombre = %s, apellido = %s, rol = %s, activo = %s
            WHERE id_usuario = %s
        """, (username, email, nombre, apellido, rol, activo, id_usuario))
        
        conexion.commit()
        filas_afectadas = cursor.rowcount
        flash(f"Filas afectadas: {filas_afectadas}") 
        
        return filas_afectadas > 0
    except Exception as e:
        flash("Error al actualizar usuario:", e)
        conexion.rollback()
        return False
    finally:
        conexion.close()


def eliminar_usuario(id_usuario):
    """Desactiva un usuario (soft delete)"""
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            UPDATE usuarios SET activo = FALSE WHERE id_usuario = %s
        """, (id_usuario,))
        conexion.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print("Error al eliminar usuario:", e)
        return False
    finally:
        conexion.close()



def limpiar_usuarios_inactivos(dias=0):
    """Elimina definitivamente usuarios inactivos. Si se pasa `dias`, se filtra por fecha de creacion."""
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        if dias > 0:
            cursor.execute("""
                DELETE FROM usuarios
                WHERE activo = FALSE AND fecha_creacion <= NOW() - INTERVAL %s DAY
            """, (dias,))
        else:
            cursor.execute("""
                DELETE FROM usuarios
                WHERE activo = FALSE
            """)
        conexion.commit()
        return cursor.rowcount
    except Exception as e:
        print("Error al limpiar usuarios inactivos:", e)
        return 0
    finally:
        conexion.close()




def cambiar_password_usuario(id_usuario, nueva_password):
    """Cambia la contraseña de un usuario"""
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        password_hash = hash_password(nueva_password)
        cursor.execute("""
            UPDATE usuarios SET password_hash = %s WHERE id_usuario = %s
        """, (password_hash, id_usuario))
        conexion.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print("Error al cambiar contraseña:", e)
        return False
    finally:
        conexion.close()






# ========== FUNCIONES DE LOGIN ==========

def autenticar_usuario(username, password):
    """Autentica un usuario basico"""
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            SELECT id_usuario, username, email, password_hash, nombre, apellido, rol
            FROM usuarios 
            WHERE username = %s AND activo = TRUE
        """, (username,))
        usuario = cursor.fetchone()
        
        if usuario and verificar_password(password, usuario[3]):
            # Actualizar ultimo login
            cursor.execute("""
                UPDATE usuarios SET ultimo_login = %s WHERE id_usuario = %s
            """, (datetime.now(), usuario[0]))
            conexion.commit()
            return usuario, "Login exitoso"
        else:
            return None, "Usuario o contraseña incorrectos"
    except Exception as e:
        print("Error en autenticacion:", e)
        return None, "Error en el servidor"
    finally:
        conexion.close()

def obtener_usuario_por_username(username):
    """Obtiene un usuario por username"""
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            SELECT id_usuario, username, email, password_hash, nombre, apellido, rol, activo
            FROM usuarios 
            WHERE username = %s
        """, (username,))
        return cursor.fetchone()
    except Exception as e:
        print("Error al obtener usuario por username:", e)
        return None
    finally:
        conexion.close()

def obtener_usuario_por_id(id_usuario):
    """Obtiene un usuario por su ID"""
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            SELECT id_usuario, username, email, nombre, apellido, rol, activo, ultimo_login
            FROM usuarios 
            WHERE id_usuario = %s AND activo = TRUE
        """, (id_usuario,))
        return cursor.fetchone()
    except Exception as e:
        print("Error al obtener usuario por ID:", e)
        return None
    finally:
        conexion.close()