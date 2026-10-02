import tkinter as tk
from tkinter import messagebox

import mysql.connector

# --- CLASE DE CONEXIÓN A BASE DE DATOS ---
class Database:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="carrito_db"
        )
        self.cursor = self.conexion.cursor(dictionary=True)

    def obtener_productos(self):
        self.cursor.execute("SELECT * FROM productos")
        return self.cursor.fetchall()

    def agregar_carrito(self, usuario_id, producto_id):
        sql = "INSERT INTO carrito (usuario_id, producto_id) VALUES (%s, %s)"
        self.cursor.execute(sql, (usuario_id, producto_id))
        self.conexion.commit()

    def agregar_favoritos(self, usuario_id, producto_id):
        sql = "INSERT INTO favoritos (usuario_id, producto_id) VALUES (%s, %s)"
        self.cursor.execute(sql, (usuario_id, producto_id))
        self.conexion.commit()


# --- CLASE PRINCIPAL DE LA INTERFAZ GRÁFICA ---
class TiendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tienda Online - POO Python")
        self.root.geometry("600x400")
        
        self.db = Database()
        self.usuario_actual_id = 1  # Simulamos que el usuario "Juan" (ID 1) ha iniciado sesión

        self.crear_interfaz()

    def crear_interfaz(self):
        # Título
        titulo = tk.Label(self.root, text="Catálogo de Productos", font=("Arial", 16, "bold"))
        titulo.pack(pady=10)

        # Contenedor de productos
        self.frame_productos = tk.Frame(self.root)
        self.frame_productos.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.cargar_productos_gui()

    def cargar_productos_gui(self):
        productos = self.db.obtener_productos()

        for prod in productos:
            # Frame para cada producto
            item_frame = tk.Frame(self.frame_productos, bd=2, relief=tk.GROOVE, padx=5, pady=5)
            item_frame.pack(fill=tk.X, pady=5)

            # Imagen (Usando Tkinter PhotoImage - requiere PNG o GIF)
            try:
                self.img = tk.PhotoImage(file=prod['imagen'])
                # Redimensionar si es muy grande (opcional)
                lbl_img = tk.Label(item_frame, image=self.img)
                lbl_img.image = self.img # Referencia para evitar que el recolector de basura la borre
                lbl_img.pack(side=tk.LEFT, padx=5)
            except Exception as e:
                lbl_img = tk.Label(item_frame, text="[Sin Imagen]")
                lbl_img.pack(side=tk.LEFT, padx=5)

            # Info del producto
            info_texto = f"{prod['nombre']}\nPrecio: ${prod['precio']}"
            lbl_info = tk.Label(item_frame, text=info_texto, font=("Arial", 12), justify=tk.LEFT)
            lbl_info.pack(side=tk.LEFT, padx=10)

            # Botones de Acción
            btn_favorito = tk.Button(item_frame, text="❤️ Favoritos", command=lambda p=prod['id']: 
self.accion_favorito(p))
            btn_favorito.pack(side=tk.RIGHT, padx=5)

            btn_carrito = tk.Button(item_frame, text="🛒 Añadir Carrito", bg="green", fg="white", command=lambda p=prod['id']: self.accion_carrito(p))
            btn_carrito.pack(side=tk.RIGHT, padx=5)

    def accion_carrito(self, producto_id):
        try:
            self.db.agregar_carrito(self.usuario_actual_id, producto_id)
            messagebox.showinfo("Éxito", "Producto añadido al carrito correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo añadir: {e}")

    def accion_favorito(self, producto_id):
        try:
            self.db.agregar_favoritos(self.usuario_actual_id, producto_id)
            messagebox.showinfo("Éxito", "Producto añadido a favoritos.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo añadir: {e}")

# --- EJECUCIÓN DE LA APLICACIÓN ---
if __name__ == "__main__":
    root = tk.Tk()
    app = TiendaApp(root)
    root.mainloop()