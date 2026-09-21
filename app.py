from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

# Inicializamos nuestra app

app = Flask(__name__)

# con esta parte de codigo solo hacemos la conexion a mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bd_pagina'
app.config['MYSQL_PORT'] = 33065

mysql = MySQL(app)

@app.route("/")
def index(): # LEER
    cur = mysql.connect.cursor() # Nota: en la imagen dice mysql.connect.cursor(), suele ser mysql.connection.cursor()
    cur.execute("SELECT * FROM user") # Ejectura la consulta de mysql
    data = cur.fetchall() # recuperamos la informacion de nuestra bd
    cur.close()
    return render_template('index.html', user=data)

@app.route('/add', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user (name, email) VALUES (%s,%s)", (name, email))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit_user(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()

        # Se agrega WHERE id = %s para que coincida con la tupla (name, email, id)
        cur.execute("UPDATE user SET name = %s, email = %s WHERE id = %s", (name, email, id))

        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE id = %s", (id,))
        data = cur.fetchone()
        cur.close()
        return render_template('edit.html', user=data)

@app.route('/delete/<int:id>')
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM user WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/search')
def buscar():
    busqueda = request.args.get('q', '').strip()

    cursor = mysql.connection.cursor()

    if busqueda:
        sql = "SELECT * FROM user WHERE name LIKE %s OR email LIKE %s"
        texto_busqueda = f"%{busqueda}%"
        cursor.execute(sql, (texto_busqueda, texto_busqueda))
    else:
        cursor.execute("SELECT * FROM user")

    usuarios = cursor.fetchall()
    cursor.close()

    return render_template('index.html', user=usuarios, busqueda=busqueda)

if __name__ == '__main__':
    app.run(debug=True)