class Usuario:
    def __init__(self, nombre, email,passw,activo,fecha):
        self.nombre = nombre
        self.email = email
        self.passwd = passw
        self.activo = activo
        self.fecha = fecha
        self.pedidos = 0