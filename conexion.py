import pymysql
from werkzeug.security import generate_password_hash, check_password_hash


HOST = "localhost"
USER = "root"
PASSWORD = "hola123"  
DB_NAME = "papebd"


def conectar_bd():
    try:
        conexion = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD
        )
        cursor = conexion.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
        print(f"Base de datos '{DB_NAME}' verificada/creada con exito.")
        
        conexion.close()
        
        conexion = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        cursor = conexion.cursor()


        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                telefono VARCHAR(20),
                email VARCHAR(100)
            );
        """)
        print("Tabla 'clientes' verificada/creada con exito.")


        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id_producto INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                categoria ENUM('Escolares', 'Oficina', 'Arte') NOT NULL,
                precio DECIMAL(10,2) NOT NULL,
                stock INT NOT NULL DEFAULT 0,
                activo TINYINT(1) DEFAULT 1,
                costo DECIMAL (10,2) DEFAULT 0
            );
        """)
        print("Tabla 'productos' verificada/creada con exito.")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id_venta INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                id_cliente INT,
                total DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
            );

        """)
        print("Tabla 'ventas' verificada/creada con exito.")



        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas_detalle (
                id_detalle INT AUTO_INCREMENT PRIMARY KEY,
                id_venta INT NOT NULL,
                id_producto INT NOT NULL,
                cantidad INT NOT NULL,
                precio_unitario DECIMAL(10,2) NOT NULL,
                total DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (id_venta) REFERENCES ventas(id_venta),
                FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
            );
        """)
        print("Tabla 'ventas_detalle' verificada/creada con exito.")


        cursor.execute("""
            CREATE TABLE IF NOT EXISTS proveedores (
                id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                rfc VARCHAR(13) UNIQUE,
                telefono VARCHAR(20),
                email VARCHAR(100) UNIQUE,
                direccion VARCHAR(150),
                creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("Tabla 'proveedores' verificada/creada con exito.")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos_proveedores (
                id_relacion INT AUTO_INCREMENT PRIMARY KEY,
                id_producto INT NOT NULL,
                id_proveedor INT NOT NULL,
                -- si borras un producto/proveedor, se borra la relacion
                FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE CASCADE,
                FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor) ON DELETE CASCADE,
                UNIQUE (id_producto, id_proveedor)  
            );
        """)
        print("Tabla 'productos_proveedores' verificada/creada con exito.")


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100),
            rol ENUM('admin', 'usuario', 'supervisor') DEFAULT 'usuario',
            activo BOOLEAN DEFAULT TRUE,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ultimo_login TIMESTAMP NULL,
            intentos_fallidos INT DEFAULT 0,
            bloqueado_hasta TIMESTAMP NULL
        );
        """)
        print("Tabla 'usuarios' verificada/creada con exito.")

        conexion.commit()
        return conexion

    except Exception as e:
        print("Error al conectar o crear la base de datos:", e)
        return None


