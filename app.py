from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from datetime import date, datetime
from models.usuario import Usuario
from models.database import BaseDatos

app = Flask(__name__)

bd = BaseDatos()

productos_col = bd.obtener_colecciones('productos')
usuarios_col = bd.obtener_colecciones('clientes')
pedidos_col = bd.obtener_colecciones('pedidos')

        #### END-POINTS ####

# Muestra dashboard.html
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    fecha = date.today()
    fecha_admin = fecha.strftime('%d/%m/%Y')


    admin ={
        'nombre_admin': 'Cristóbal',
        'tienda': 'TecnoMarket',
        'fecha': fecha_admin
    }

    productos = list(productos_col.find())
    clientes = list(usuarios_col.find())
    pedidos = list(pedidos_col.find())


    # Calcular ingresos totales por ventas
    ingresos = 0.0

    for pedido in pedidos:
        ingresos += pedido['total']

    # Calcular total de productos en stock
    total_stock = 0

    for producto in productos:
        total_stock += producto['stock']

    # Calcular clientes activos y Mostrar el cliente con más pedidos

    active = 0

    mas_pedidos = {
        'nombre': '',
        'cantidad': 0
    }

    for cliente in clientes:
        if cliente['activo']:
            active +=1

        if cliente['pedidos'] > mas_pedidos['cantidad']:
            mas_pedidos['nombre'] = cliente['nombre']
            mas_pedidos['cantidad'] = cliente['pedidos']

    return render_template('dashboard.html', **admin,
                           productos=productos, clientes=clientes, pedidos_clientes=pedidos,
                           ingresos=ingresos, total_productos=total_stock,
                           active=active, mas_pedidos=mas_pedidos)

# Añadir productos a la BBDD
@app.route('/add_producto', methods=['GET', 'POST'])
def add_producto():
    mensaje = ''

    if request.method == 'POST':

        nombre = request.form['nombre'].title()
        precio = float(request.form['precio'])
        categoria = request.form['categoria'].title()
        stock = int(request.form['stock'])

        productos_col.insert_one({
            'nombre': nombre,
            'precio': precio,
            'categoria': categoria,
            'stock': stock,
        })
        mensaje = f'El producto {nombre} ha sido añadido correctamente.'

    return render_template('add_producto.html', mensaje=mensaje)

# Listado de los productos registrados en la BBDD
@app.route('/lista_productos', methods=['GET', 'POST'])
def lista_productos():
    productos = list(productos_col.find())
    return render_template('lista_productos.html', lista_productos=productos)

# Muestra detalle de los productos
@app.route('/productos/<id_producto>', methods=['GET', 'POST'])
def detalle_producto(id_producto):
    producto = productos_col.find_one({"_id": ObjectId(id_producto)})
    if producto:
        return render_template('detalle_producto.html', producto=producto)

# Editar productos
@app.route('/productos/<id_producto>/editar', methods=['POST'])
def editar_producto(id_producto):
    nombre = request.form['nombre'].title()
    precio = float(request.form['precio'])
    categoria = request.form['categoria'].title()
    stock = int(request.form['stock'])

    productos_col.update_one(
        {'_id' : ObjectId(id_producto)},
        {'$set' :
            {'nombre': nombre,
             'precio': precio,
             'categoria': categoria,
             'stock': stock,}
        }
    )

    return redirect(url_for('detalle_producto', id_producto=id_producto))

# Borrar productos
@app.route('/productos/<id_producto>/borrar', methods=['POST'])
def borrar_producto(id_producto):
    productos_col.delete_one({'_id': ObjectId(id_producto)})
    return redirect(url_for('lista_productos', id_producto=id_producto))


# Añadir usuarios a la BBDD
@app.route('/registro-usuario', methods=['GET', 'POST'])
def registro_usuario():
    mensaje_user = ''

    if request.method == 'POST':
        nombre_user = request.form['nombre_user'].title()
        email_user = request.form['email_user'].lower()
        fecha_user = datetime.today().strftime('%d/%m/%Y')
        activo_user = request.form['activo_user']
        passw_user = request.form['passw_user']


        usuario = Usuario(nombre_user, email_user, passw_user, activo_user,fecha_user)

        usuarios_col.insert_one(usuario.__dict__) # Convierte el objeto a dict para meterlo en MongoDB

        mensaje_user = f'El usuario {nombre_user} ha sido añadido correctamente.'

    return render_template('registro_usuario.html', mensaje_user=mensaje_user)

# Listado de los usuarios registrados en la BBDD
@app.route('/lista_usuario', methods=['GET', 'POST'])
def lista_usuario():
    clientes = list(usuarios_col.find())
    return render_template('lista_usuarios.html', lista_clientes=clientes)

# Añadir pedidos
@app.route('/add_pedido', methods=['GET', 'POST'])
def add_pedido():
    mensaje = ''
    clientes = list(usuarios_col.find())

    if request.method == 'POST':

        cliente_id = request.form.get('cliente', '').strip()
        total = float(request.form.get('total', 0))

        if not cliente_id:
            mensaje = 'Selecciona un cliente'
        else:
            try:
                cliente = usuarios_col.find_one({'_id': ObjectId(cliente_id)})

                if not cliente:
                    mensaje = 'El cliente no existe'
                else:
                    pedido= {
                        'cliente' : cliente['nombre'],
                        'total' : total,
                        'fecha' : datetime.today().strftime('%d/%m/%Y'),
                    }

                    print(f'Inserto pedido: {pedido}')

                    pedidos_col.insert_one(pedido)

                    # Le sumamos 1 al campo num_pedidos del cliente
                    usuarios_col.update_one(
                        {'_id': cliente['_id']},
                        {'$inc': {'pedidos': 1}}
                    )

                    mensaje = 'Pedido añadido correctamente'

            except Exception as e:
                mensaje = f'Error no determinado: {e}'

    return render_template('add_pedido.html', mensaje=mensaje, clientes=clientes)


# Manejador de error 404 - Page not found
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', mensaje='Página no encontrada.')

# Manejador de error 500 - Error en el servidor
@app.errorhandler(500)
def not_found(e):
    return render_template('404.html', mensaje='Error en el servidor')


if __name__ == '__main__':
    app.run()