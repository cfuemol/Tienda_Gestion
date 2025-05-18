from pymongo import MongoClient
import os
from dotenv import load_dotenv

class BaseDatos:
    def __init__(self):
        try:
            # Cargar las variables de entorno
            load_dotenv()
            mong_url = os.getenv("MONGO_URL")

            # Conexión a MongoDB
            self.client = MongoClient(mong_url)
            self.db = self.client["Tienda_Gestion"]

            self.inicializar_colecciones()

            print("✅ Conexión a MongoDB establecida correctamente.")

        except Exception as e:
            print(f"\n❌ Falló la conexión a MongoDB: {e}")

    def inicializar_colecciones(self):
        colecciones = ['clientes', 'productos', 'pedidos']
        col_existentes = self.db.list_collection_names()

        for coleccion in colecciones:
            if coleccion not in col_existentes:
                self.db.create_collection(coleccion)
                print(f"📁 Colección '{coleccion}' creada.")

    # Nos devuelve la coleccion (tabla) cuyo nombre le especifiquemos
    def obtener_colecciones(self,nombre):
        return self.db[nombre]
