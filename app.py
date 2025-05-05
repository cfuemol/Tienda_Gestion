from flask import Flask, render_template
from datetime import date

app = Flask(__name__)


@app.route('/dashboard')
def dashboard():
    admin = {
        'nombre_admin' : 'Francisco',
        'tienda' : 'TecnoMarket',
        'fecha' : date.today()
    }

    productos = [
        {'nombre' : 'Teclado mecánico', 'precio' : 45.00, 'categoria' : 'Periféricos', 'stock' : 5},
        {'nombre': 'Monitor 24\"', 'precio' : 120.99, 'categoria' : 'Monitores', 'stock' : 2},
        {'nombre': 'Webcam HD', 'precio': 39.90, 'categoria' : 'Periféricos', 'stock': 0}
    ]

    clientes = [
        {'nombre' : 'Ana', 'email' : 'ana@mail.com', 'activo' : True, 'pedidos' : 12},
        {'nombre' : 'Luis', 'email' : 'luis@mail.com', 'activo' : False, 'pedidos' : 3},
        {'nombre' : 'Carmen', 'email' : 'carmen@mail.com', 'activo' : True, 'pedidos' : 7},
        {'nombre' : 'Pedro', 'email' : 'pedro@mail.com', 'activo' : True, 'pedidos' : 10}
    ]

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
        if cliente['activo']:
            active +=1

        if cliente['pedidos'] > mas_pedidos['cantidad']:
            mas_pedidos['nombre'] = cliente['nombre']
            mas_pedidos['cantidad'] = cliente['pedidos']


    return render_template('dashboard.html', **admin,
                           productos=productos, clientes=clientes, pedidos_clientes=pedidos_clientes,
                           ingresos=ingresos, total_productos=total_productos,
                           active=active, mas_pedidos=mas_pedidos)

if __name__ == '__main__':
    app.run()
