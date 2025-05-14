from flask import Flask, render_template, request
from datetime import date
from pymongo import MongoClient

app = Flask(__name__)
cliente = MongoClient('mongodb+srv://cfuemol584:SPgHlmWg5fG2eOgR@flaskmongodb.haghvj1.mongodb.net/?tls=true')
app.db = cliente.Tienda_Gestion

productos = [producto for producto in app.db.productos.find({})]
clientes = [cliente for cliente in app.db.clientes.find({})]

        #### END-POINTS ####

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    admin = {
        'nombre_admin' : 'Francisco',
        'tienda' : 'TecnoMarket',
        'fecha' : date.today()
    }

    pedidos_clientes = [
        # Pedidos de Ana
        {'cliente': 'Ana', 'total': 112.97, 'fecha': '2024-12-22'},
        {'cliente': 'Ana', 'total': 212.97, 'fecha': '2024-12-20'},
        {'cliente': 'Ana', 'total': 133.12, 'fecha': '2024-12-27'},
        {'cliente': 'Ana', 'total': 192.87, 'fecha': '2024-12-30'},
        {'cliente': 'Ana', 'total': 212.11, 'fecha': '2025-01-04'},
        {'cliente': 'Ana', 'total': 234.22, 'fecha': '2025-01-08'},
        {'cliente': 'Ana', 'total': 322.97, 'fecha': '2025-01-22'},
        {'cliente': 'Ana', 'total': 92.22, 'fecha': '2025-01-31'},
        {'cliente': 'Ana', 'total': 12.97, 'fecha': '2025-02-12'},
        {'cliente': 'Ana', 'total': 11.17, 'fecha': '2025-02-22'},
        {'cliente': 'Ana', 'total': 442.35, 'fecha': '2025-03-04'},
        {'cliente': 'Ana', 'total': 112.97, 'fecha': '2025-04-12'},

        # Pedidos de Luis
        {'cliente': 'Luis', 'total': 92.97, 'fecha': '2024-12-22'},
        {'cliente': 'Luis', 'total': 192.97, 'fecha': '2024-12-26'},
        {'cliente': 'Luis', 'total': 79.97, 'fecha': '2024-12-31'},

        # Pedidos de Carmen
        {'cliente': 'Carmen', 'total': 32.97, 'fecha': '2024-12-02'},
        {'cliente': 'Carmen', 'total': 43.97, 'fecha': '2024-12-20'},
        {'cliente': 'Carmen', 'total': 45.00, 'fecha': '2024-12-26'},
        {'cliente': 'Carmen', 'total': 132.97, 'fecha': '2024-12-31'},
        {'cliente': 'Carmen', 'total': 177.88, 'fecha': '2025-02-12'},
        {'cliente': 'Carmen', 'total': 199.99, 'fecha': '2025-04-22'},
        {'cliente': 'Carmen', 'total': 149.99, 'fecha': '2025-05-01'},

        # Pedidos de Pedro
        {'cliente': 'Pedro', 'total': 88.33, 'fecha': '2024-07-22'},
        {'cliente': 'Pedro', 'total': 127.25, 'fecha': '2024-08-12'},
        {'cliente': 'Pedro', 'total': 223.39, 'fecha': '2024-09-19'},
        {'cliente': 'Pedro', 'total': 57.75, 'fecha': '2024-10-22'},
        {'cliente': 'Pedro', 'total': 79.95, 'fecha': '2024-11-04'},
        {'cliente': 'Pedro', 'total': 83.27, 'fecha': '2024-12-29'},
        {'cliente': 'Pedro', 'total': 295.95, 'fecha': '2025-01-11'},
        {'cliente': 'Pedro', 'total': 7.95, 'fecha': '2025-02-25'},
        {'cliente': 'Pedro', 'total': 499.95, 'fecha': '2025-03-09'},
        {'cliente': 'Pedro', 'total': 29.95, 'fecha': '2025-04-30'}

    ]

    # Calcular ingresos totales por ventas
    ingresos = 0.0

    for pedido in pedidos_clientes:
        ingresos += pedido['total']

    # Calcular total de productos en stock
    total_productos = 0

    for producto in productos:
        total_productos += producto['stock']

    # Calcular clientes activos y Mostrar el cliente con más pedidos

    active = 0

    mas_pedidos = {
        'nombre': '',
        'cantidad': 0
    }

    for cliente in clientes:
        if cliente['estado']:
            active +=1

        if cliente['pedidos'] > mas_pedidos['cantidad']:
            mas_pedidos['nombre'] = cliente['nombre']
            mas_pedidos['cantidad'] = cliente['pedidos']

    # Añadir datos del formulario a la lista de productos de la tienda

            add_client = {}

            client = dict(request.form)
            add_client['nombre'] = client['nombre_cliente'].title()
            add_client['email'] = client['email_cliente'].lower()
            add_client['estado'] = False
            add_client['pedidos'] = 0

            clientes.append(add_client)
            app.db.clientes.insert_one(add_client)

    return render_template('dashboard.html', **admin,
                           productos=productos, clientes=clientes, pedidos_clientes=pedidos_clientes,
                           ingresos=ingresos, total_productos=total_productos,
                           active=active, mas_pedidos=mas_pedidos)

@app.route('/add_producto', methods=['GET', 'POST'])
def add_producto():
    mensaje = ''

    if request.method == 'POST':

        nombre = request.form['nombre'].title()
        precio = float(request.form['precio'])
        categoria = request.form['categoria'].title()
        stock = int(request.form['stock'])

        app.db.productos.insert_one({
            'nombre': nombre,
            'precio': precio,
            'categoria': categoria,
            'stock': stock,
        })
        mensaje = f'El producto {nombre} ha sido añadido correctamente.'


    return render_template('add_producto.html', mensaje=mensaje)

@app.route('/lista_productos', methods=['GET', 'POST'])
def lista_productos():
    return render_template('lista_productos.html', productos=productos)

@app.route('/productos/<id_producto>', methods=['GET', 'POST'])
def producto(id_producto):
    product_found = None
    for producto in productos:
        if producto[0] == id_producto:
            product_found = producto
            break

    if product_found:
        return render_template('detalle_producto.html', producto=product_found)
    else:
        return render_template('404.html')
## Crear los endpoints a la misma vez que las webs
# correspondientes y en el nav##


if __name__ == '__main__':
    app.run()