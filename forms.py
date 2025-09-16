from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField, PasswordField, SelectField, DecimalField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo, NumberRange, Regexp

# Formulario Cliente
class ClienteForm(FlaskForm):
    nombre = StringField("nombre")
    telefono = StringField("telefono")
    email = StringField("email")
    submit = SubmitField("guardar")

# Formulario productos
class ProductoForm(FlaskForm):
    nombre = StringField("Nombre")
    categoria = SelectField("Categoria")
    precio = DecimalField("Precio")
    stock = IntegerField("Stock")
    costo = DecimalField("costo") #costo en cada uno
    submit = SubmitField("Guardar")

class NuevaVentaForm(FlaskForm):
    id_cliente = SelectField("Cliente")
   # No se definen productos aqui directamente, se pueden procesar manualmente en la vista
    submit = SubmitField("Guardar Venta")

class ProveedorForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    rfc = StringField("RFC", validators=[
        DataRequired(),
        Length(min=12, max=13, message="El RFC debe tener entre 12 y 13 caracteres"),
        Regexp(r"^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$", message="Formato de RFC invalido")
    ])
    telefono = StringField("Telefono", validators=[Length(max=10)])
    email = StringField("Email", validators=[Email(), Length(max=100)])
    direccion = StringField("Direccion", validators=[
        DataRequired(message="La direccion es requerida"),
        Length(min=10, max=150, message="La direccion debe tener entre 10 y 150 caracteres"),
        Regexp(r"^[a-zA-Z0-9\s,.-aeiouñuaeiouÑu#°]+$", 
               message="La direccion contiene caracteres no validos")
                ])    
    submit = SubmitField("Guardar")


class AsociarProveedorForm(FlaskForm):
    id_proveedor = SelectField(
        'Seleccionar Proveedor',
        choices=[],  # Se llenaran dinamicamente en la vista
        validators=[DataRequired(message="Debe seleccionar un proveedor")],
        render_kw={"id": "id_proveedor"}
    )
    
    submit = SubmitField('Asociar Proveedor')
    
    def __init__(self, proveedores=None, *args, **kwargs):
        super(AsociarProveedorForm, self).__init__(*args, **kwargs)
        if proveedores:
            # Crear las opciones para el SelectField
            self.id_proveedor.choices = [('', '-- Seleccione un proveedor --')] + [
                (str(prov[0]), f"{prov[1]} (RFC: {prov[2]})") for prov in proveedores
            ]






####
####
####
####
####


class UsuarioForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    apellido = StringField('Apellido', validators=[Optional(), Length(max=100)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    rol = SelectField(
        'Rol',
        choices=[('usuario', 'Usuario'), ('supervisor', 'Supervisor'), ('admin', 'Administrador')],
        default='usuario'
    )
    activo = BooleanField('Usuario Activo', default=True)
    submit = SubmitField('Guardar Usuario')




class EditarUsuarioForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    apellido = StringField('Apellido', validators=[Optional(), Length(max=100)])
    rol = SelectField(
        'Rol',
        choices=[('usuario', 'Usuario'), ('supervisor', 'Supervisor'), ('admin', 'Administrador')]
    )
    activo = BooleanField('Usuario Activo')
    submit = SubmitField('Actualizar Usuario')



class CambiarPasswordForm(FlaskForm):
    nueva_password = PasswordField(
        'Nueva Contraseña',
        validators=[DataRequired(message="La nueva contraseña es requerida"),
                   Length(min=6, message="La contraseña debe tener al menos 6 caracteres")]
    )
    confirmar_password = PasswordField(
        'Confirmar Nueva Contraseña',
        validators=[DataRequired(message="Debe confirmar la nueva contraseña"),
                   EqualTo('nueva_password', message="Las contraseñas no coinciden")]
    )
    submit = SubmitField('Cambiar Contraseña')

class LoginSimpleForm(FlaskForm):
    username = StringField(
        'Usuario',
        validators=[DataRequired(message="El usuario es requerido")]
    )
    password = PasswordField(
        'Contraseña',
        validators=[DataRequired(message="La contraseña es requerida")]
    )
    submit = SubmitField('Iniciar Sesion')