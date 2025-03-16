from flask import Flask, render_template, request, redirect, jsonify  
import mysql.connector  

app = Flask(__name__)  

# Función para obtener la conexión a la base de datos MySQL.
def get_db_connection():  
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="medicamentos_db"
    )

@app.route('/')
def home():
    conn = get_db_connection() 
    cursor = conn.cursor()  # Creación de un cursor para interactuar con la base de datos.
    cursor.execute("SELECT * FROM medicamentos")  # Ejecutar una consulta para obtener todos los medicamentos.
    medicamentos = cursor.fetchall()  # Obtener los resultados.
    conn.close()  # Cerrar la conexión a la base de datos.
    return render_template('index.html', medicamentos=medicamentos)  # Renderizar la plantilla y pasar los medicamentos.

@app.route('/add', methods=['POST'])  
def add():
    # Obtener los datos del formulario
    nombre = request.form['nombre']  
    hora = request.form['hora']  
    duracion = request.form['duracion'] 
    
    if not nombre or not hora or not duracion:  # Verificar que todos los campos estén completos.
        return jsonify({"error": "Todos los campos son obligatorios"}), 400  
    
    conn = get_db_connection()  
    cursor = conn.cursor()  
    cursor.execute("INSERT INTO medicamentos (nombre, hora, duracion) VALUES (%s, %s, %s)", (nombre, hora, duracion))  
    conn.commit()  # Confirmar los cambios realizados.
    conn.close()
    return redirect('/')  # Redirigir a la página principal después de agregar el medicamento.

@app.route('/update/<int:id>', methods=['POST'])  
def update(id):
    nombre = request.form['nombre']  # Obtener los nuevos datos.
    hora = request.form['hora']  
    duracion = request.form['duracion'] 
    
    if not nombre or not hora or not duracion:  # Verificar que todos los campos estén completos.
        return jsonify({"error": "Todos los campos son obligatorios"}), 400  
    
    conn = get_db_connection()  
    cursor = conn.cursor()  
    cursor.execute("UPDATE medicamentos SET nombre=%s, hora=%s, duracion=%s WHERE id=%s", (nombre, hora, duracion, id))  
    conn.commit()  # Confirmar los cambios realizados.
    conn.close()
    return redirect('/')  # Redirigir a la página principal después de actualizar.

@app.route('/delete/<int:id>', methods=['POST'])  
def delete(id):
    conn = get_db_connection() 
    cursor = conn.cursor()  
    cursor.execute("DELETE FROM medicamentos WHERE id = %s", (id,))  # Eliminar el medicamento por ID.
    conn.commit()  # Confirmar la eliminación.
    conn.close()
    return jsonify({"message": "Eliminado correctamente"})  # Confirmar que el medicamento fue eliminado.

if __name__ == '__main__':  
    app.run(debug=True)
