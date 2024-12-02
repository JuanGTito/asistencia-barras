from flask import Flask, render_template, request, redirect, url_for, jsonify
import query  
from camara import scan_code 

app = Flask(__name__)

@app.route('/')
def index():
    empleados = query.obtener_empleados()  # Obtener empleados
    return render_template('index.html', empleados=empleados)

@app.route('/registrar', methods=['POST'])
def registrar_empleado():
    codigo_empleado = request.form['codigo_empleado']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    dni = request.form['dni']
    fecha_ingreso = request.form['fecha_ingreso']
    cargo = request.form['cargo']
    estado = request.form['estado']
    
    query.registrar_empleado(codigo_empleado, nombre, apellido, dni, fecha_ingreso, cargo, estado)
    
    return redirect(url_for('home'))

@app.route('/asistencia', methods=['POST'])
def registrar_asistencia():

        codigo_empleado = request.form['codigo_empleado']
        fecha = request.form['fecha']
        hora_entrada = request.form['hora_entrada']
        hora_salida = request.form['hora_salida']

        query.registrar_asistencia(codigo_empleado, fecha, hora_entrada, hora_salida)

        return redirect(url_for('home'))


@app.route('/iniciar-scanner', methods=['GET'])
def iniciar_scanner():

    codigo_empleado = scan_code()
    if codigo_empleado:
        return jsonify(codigo_empleado)
    else:
        return jsonify({"message": "No se detectó ningún código de barras."})

@app.route('/reportes', methods=['GET'])
def generar_reportes():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    reportes = query.generar_reportes(fecha_inicio, fecha_fin)
    return render_template('reportes.html', reportes=reportes)

if __name__ == '__main__':
    app.run(debug=True)