import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="sistema_asistencia"
    )
