from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configurar la conexión a la base de datos
db_config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'fotografia'
}

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para mostrar todos los contactos
@app.route('/contactos')
def contactos():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contactos")
    contactos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('contactos.html', contactos=contactos)

# Ruta para manejar el formulario de contacto
@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        fecha_evento = request.form['fecha_evento']
        mensaje = request.form['mensaje']
        
        # Insertar datos en la base de datos
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contactos (nombre, email, telefono, fecha_evento, mensaje) VALUES (%s, %s, %s, %s, %s)", 
                       (nombre, email, telefono, fecha_evento, mensaje))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('contactos'))
    return render_template('contacto.html')

# Ruta para editar un contacto
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contactos WHERE id = %s", (id,))
    contacto = cursor.fetchone()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        fecha_evento = request.form['fecha_evento']
        mensaje = request.form['mensaje']
        
        cursor.execute("""
            UPDATE contactos
            SET nombre = %s, email = %s, telefono = %s, fecha_evento = %s, mensaje = %s
            WHERE id = %s
        """, (nombre, email, telefono, fecha_evento, mensaje, id))
        conn.commit()
        return redirect(url_for('contactos'))
    
    cursor.close()
    conn.close()
    return render_template('editar.html', contacto=contacto)

# Ruta para eliminar un contacto
@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contactos WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('contactos'))

if __name__ == '__main__':
    app.run(debug=True)

