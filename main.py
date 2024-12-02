from flask import Flask, render_template, request, redirect, url_for, jsonify
import query  # Asegúrate de tener funciones para interactuar con la base de datos.
from camara import scan_code  # Importa la función de escaneo de código

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar_empleado():
    nombre = request.form['nombre']
    dni = request.form['dni']
    cargo = request.form['cargo']
    # Llama a la función para registrar al empleado en la base de datos.
    query.registrar_empleado(nombre, dni, cargo)
    return redirect(url_for('home'))

@app.route('/asistencia', methods=['POST'])
def registrar_asistencia():
    # Si quieres usar el código de barras escaneado:
        codigo_empleado = request.form['codigo_empleado']
        fecha = request.form['fecha']
        hora_entrada = request.form['hora_entrada']
        hora_salida = request.form['hora_salida']
        # Llama a la función para registrar la asistencia en la base de datos.
        query.registrar_asistencia(codigo_empleado, fecha, hora_entrada, hora_salida)

        return redirect(url_for('home'))

# Nueva ruta para iniciar el escaneo del código de barras
@app.route('/iniciar-scanner', methods=['GET'])
def iniciar_scanner():
    # Llama a la función para iniciar el escaneo de código de barras.
    codigo_empleado = scan_code()
    if codigo_empleado:
        return jsonify(codigo_empleado)
    else:
        return jsonify({"message": "No se detectó ningún código de barras."})

@app.route('/reportes', methods=['GET'])
def generar_reportes():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    # Llama a la función para generar los reportes.
    reportes = query.generar_reportes(fecha_inicio, fecha_fin)
    return render_template('reportes.html', reportes=reportes)

if __name__ == '__main__':
    app.run(debug=True)