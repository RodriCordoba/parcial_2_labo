import sqlite3
NOMBRE_BASE_DE_DATOS = "ranking.db"

def crear_tablas_db():
    try:
        conexion = sqlite3.connect(NOMBRE_BASE_DE_DATOS)
        conexion.execute('''CREATE TABLE IF NOT EXISTS jugadores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT,
                        puntuacion INTEGER
                    )''')
        conexion.close()
    except sqlite3.OperationalError:
        print("La tabla personajes ya existe")

def insertar_jugador(nombre, puntuacion):
    try:
        conexion = sqlite3.connect(NOMBRE_BASE_DE_DATOS)
        conexion.execute("INSERT INTO jugadores (nombre, puntuacion) VALUES (?, ?)", (nombre, puntuacion))
        conexion.commit()
        conexion.close()
    except:
        print("Error")

def obtener_ranking():
    try:
        conexion = sqlite3.connect(NOMBRE_BASE_DE_DATOS)
        cursor = conexion.execute("SELECT nombre, puntuacion FROM jugadores ORDER BY puntuacion DESC")
        ranking = cursor.fetchall()
        conexion.close()
        return ranking
    except:
        print("Error")
