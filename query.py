from conexion import obtener_conexion
from datetime import datetime

def registrar_empleado(codigo_empleado, nombre, apellido, dni, fecha_ingreso, cargo, estado):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Consulta SQL para insertar el empleado en la base de datos
    query = """
    INSERT INTO empleados (codigo_empleado, nombre, apellido, dni, fecha_ingreso, cargo, estado)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    # Ejecutar la consulta con los datos proporcionados
    cursor.execute(query, (codigo_empleado, nombre, apellido, dni, fecha_ingreso, cargo, estado))
    
    # Confirmar la transacción
    conexion.commit()

    # Cerrar la conexión
    cursor.close()
    conexion.close()

def actualizar_empleado(codigo_empleado, nombre=None, apellido=None, dni=None, cargo=None, estado=None):
    conn = obtener_conexion()
    cursor = conn.cursor()
    query = "UPDATE empleados SET"
    fields = []
    params = []

    if nombre:
        fields.append("nombre = %s")
        params.append(nombre)
    if apellido:
        fields.append("apellido = %s")
        params.append(apellido)
    if dni:
        fields.append("dni = %s")
        params.append(dni)
    if cargo:
        fields.append("cargo = %s")
        params.append(cargo)
    if estado:
        fields.append("estado = %s")
        params.append(estado)

    query += ", ".join(fields) + " WHERE codigo_empleado = %s"
    params.append(codigo_empleado)

    cursor.execute(query, tuple(params))
    conn.commit()
    cursor.close()
    conn.close()
    print("Empleado actualizado correctamente.")

def obtener_empleados():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Consulta SQL para obtener todos los empleados
    query = "SELECT codigo_empleado, nombre, apellido, cargo FROM empleados"
    
    # Ejecutar la consulta
    cursor.execute(query)
    
    # Obtener todos los resultados
    empleados = cursor.fetchall()
    
    # Cerrar la conexión
    cursor.close()
    conexion.close()
    
    return empleados

def eliminar_empleado(codigo_empleado):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleados WHERE codigo_empleado = %s", (codigo_empleado,))
    conn.commit()
    cursor.close()
    conn.close()
    print("Empleado eliminado correctamente.")


def registrar_asistencia(codigo_empleado, fecha, hora_entrada, hora_salida=None, estado='asistió'):
    # Conectar a la base de datos
    fecha = datetime.now().strftime('%Y-%m-%d')
    conn = obtener_conexion()
    cursor = conn.cursor()

    # Obtener el número de asistencias previas del empleado
    cursor.execute('''
        SELECT COUNT(*) FROM asistencias WHERE codigo_empleado = %s
    ''', (codigo_empleado,))
    contador_asistencias = cursor.fetchone()[0] + 1  # Iniciar el contador desde 1

    # Generar el código de asistencia como 'A' seguido del código del empleado y el contador
    codigo_asistencia = f"A{codigo_empleado}{str(contador_asistencias).zfill(4)}"  # Rellenar con ceros a la izquierda si es necesario

    # Si no se proporciona hora_salida, se deja como NULL en la base de datos
    if hora_salida is None:
        hora_salida = None

    # Insertar el registro de asistencia en la base de datos
    query = '''
        INSERT INTO asistencias (codigo_asistencia, codigo_empleado, fecha, hora_entrada, hora_salida, estado)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(query, (codigo_asistencia, codigo_empleado, fecha, hora_entrada, hora_salida, estado))
    conn.commit()
    cursor.close()
    conn.close()
    
    print("Asistencia registrada correctamente.")

def obtener_asistencias(fecha_inicio=None, fecha_fin=None):
    conn = obtener_conexion()
    cursor = conn.cursor()
    if fecha_inicio and fecha_fin:
        query = '''
            SELECT * FROM asistencias
            WHERE fecha BETWEEN %s AND %s
        '''
        cursor.execute(query, (fecha_inicio, fecha_fin))
    else:
        cursor.execute("SELECT * FROM asistencias")
    asistencias = cursor.fetchall()
    cursor.close()
    conn.close()
    return asistencias

# Consultas para la tabla "reportes"
def generar_reporte(codigo_reporte, codigo_empleado, fecha_inicio, fecha_fin):
    conn = obtener_conexion()
    cursor = conn.cursor()

    # Calcular totales
    cursor.execute('''
        SELECT
            COUNT(*) AS total_asistencias,
            SUM(CASE WHEN estado = 'tarde' THEN 1 ELSE 0 END) AS total_tardanzas,
            SUM(CASE WHEN estado = 'no asistió' THEN 1 ELSE 0 END) AS total_ausencias
        FROM asistencias
        WHERE codigo_empleado = %s AND fecha BETWEEN %s AND %s
    ''', (codigo_empleado, fecha_inicio, fecha_fin))

    resultado = cursor.fetchone()
    total_asistencias = resultado[0]
    total_tardanzas = resultado[1]
    total_ausencias = resultado[2]

    # Insertar el reporte
    query = '''
        INSERT INTO reportes (codigo_reporte, codigo_empleado, fecha_inicio, fecha_fin, total_asistencias, total_tardanzas, total_ausencias)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(query, (codigo_reporte, codigo_empleado, fecha_inicio, fecha_fin, total_asistencias, total_tardanzas, total_ausencias))
    conn.commit()
    cursor.close()
    conn.close()
    print("Reporte generado correctamente.")
