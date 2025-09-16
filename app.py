import conexion
from flask import Flask, render_template, request, redirect, url_for, flash, session
from conexion import conectar_bd
from datetime import datetime, timedelta
from flask_session import Session

# Importar modelo de usuarios
from models.usuarios_modelo import autenticar_usuario, obtener_usuario_por_id


app = Flask(__name__)

# Configuracion de sesiones
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'tu-clave-secreta-super-segura-cambiala'
Session(app)

# Registrar blueprints existentes
from routes.clientes import clientes_bp
app.register_blueprint(clientes_bp)

from routes.productos import productos_bp
app.register_blueprint(productos_bp)

from routes.ventas import ventas_bp
app.register_blueprint(ventas_bp)

from routes.proveedores import proveedores_bp
app.register_blueprint(proveedores_bp)

from routes.productos_proveedores import productos_proveedores_bp
app.register_blueprint(productos_proveedores_bp)

from routes.auth import usuarios_bp
app.register_blueprint(usuarios_bp)

from routes.backup import backup_bp
app.register_blueprint(backup_bp)

from routes.reportes import reportes_bp
app.register_blueprint(reportes_bp)



# Filtros de Jinja
@app.template_filter('datetimeformat')
def datetimeformat(value, format="%d/%m/%Y %H:%M"):
    if isinstance(value, datetime):
        return value.strftime(format)
    return value

@app.template_filter('currency')
def currency(value):
    try:
        return f"${float(value):,.2f}"
    except (ValueError, TypeError):
        return value

# Funcion para verificar si esta logueado
def esta_logueado():
    return 'user_id' in session and session['user_id'] is not None

# Context processor para hacer disponible info del usuario
@app.context_processor
def inject_user():
    if esta_logueado():
        usuario = obtener_usuario_por_id(session['user_id'])
        return {
            'esta_logueado': True,
            'usuario_actual': {
                'id': session['user_id'],
                'username': session.get('username', ''),
                'nombre': session.get('nombre', ''),
                'rol': session.get('rol', 'usuario')
            }
        }
    return {'esta_logueado': False, 'usuario_actual': None}

# Ruta principal
@app.route("/")
def index():
    try:
        if not esta_logueado():
            return redirect("/login")
        return render_template("index.html")
    except Exception as e:
        return f"Error al cargar pagina principal: {e}"
    

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'user_id' in session:
        return redirect("/")
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if username and password:
            from models.usuarios_modelo import autenticar_usuario
            usuario, mensaje = autenticar_usuario(username, password)
            
            if usuario:
                session["user_id"] = usuario[0]
                session["username"] = usuario[1]
                session["nombre"] = usuario[4]
                session["rol"] = usuario[6]
                session["name"] = usuario[4]  # Mantener compatibilidad
                flash(f"Bienvenido, {usuario[4]}!", "success")
                return redirect("/")
            else:
                flash(mensaje, "danger")
        else:
            flash("Ingrese usuario y contraseña", "warning")
    
    return render_template("login.html")



@app.route("/logout")
def logout():
    session.clear()
    flash("Sesion cerrada correctamente", "info")
    return redirect("/login")

@app.route("/usr_components/usuario_form", methods=["GET", "POST"])
def registro():
    if not esta_logueado() or session.get('rol') != 'admin':
        flash("No tiene permisos para registrar usuarios", "danger")
        return redirect("/")
    
    if request.method == "POST":
        from models.usuarios_modelo import crear_usuario
        
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        rol = request.form.get("rol", "usuario")
        
        if crear_usuario(username, email, password, nombre, apellido, rol):
            flash(f"Usuario {username} creado correctamente", "success")
        else:
            flash("Error al crear usuario. Verifique que el username y email no existan", "danger")
    
    return render_template("registro.html")

# Crear usuario admin si no existe
def crear_admin_inicial():
    from models.usuarios_modelo import obtener_usuario_por_username, crear_usuario
    
    try:
        admin_existente = obtener_usuario_por_username('admin')
        if not admin_existente:
            crear_usuario('admin', 'admin@empresa.com', 'admin123', 'Administrador', rol='admin')
            print("Usuario admin creado: admin/admin123")
    except Exception as e:
        print(f"Error al verificar usuario admin: {e}")

if __name__ == "__main__":
    # Crear admin inicial si no existe
    crear_admin_inicial()

    
    app.run(debug=True)