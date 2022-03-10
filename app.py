from flask import Flask
from flask import render_template,request,redirect,url_for #render_template: muestra vista #request #redirect
from flaskext.mysql import MySQL
from flask import send_from_directory

from datetime import datetime
import os #importar modulo sistema operativo

app=Flask(__name__)

mysql= MySQL()
app.config ['MySQL_DATABASE_HOST']='localhost'
app.config ['MySQL_DATABASE_USER']='root'
app.config ['MySQL_DATABASE_PASSWORD']=''
app.config ['MYSQL_DATABASE_DB'] = 'sistema'
mysql.init_app(app)

CARPETA= os.path.join('uploads')
app.config ['CARPETA']=CARPETA

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
   return send_from_directory(app.config ['CARPETA'],nombreFoto)

@app.route('/')
def index():
    
    sql= "SELECT * FROM `maestros`;"
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)

    maestros=cursor.fetchall()
    print()

    conn.commit()

    return render_template('maestros/index.html',maestros=maestros)

@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor=conn.cursor()

    cursor.execute("SELECT Foto FROM maestros WHERE id=%s",id)
    fila=cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))

    cursor.execute("DELETE FROM maestros WHERE id=%s",(id))
    conn.commit()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):

    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM maestros WHERE id=%s",(id))
    maestros=cursor.fetchall()
    conn.commit()
    return render_template('maestros/edit.html',maestros=maestros)

@app.route('/update', methods=['POST'])
def update():

    _nombre=request.form['txtNombre']
    _apellido=request.form['txtApellido']
    _correo=request.form['txtCorreo']
    _materia=request.form['txtMateria']
    _foto=request.files['txtFoto']
    id=request.form['txtID']

    sql= "UPDATE maestros SET Nombre=%s,Apellido=%s,Correo=%s,Materia=%s WHERE id=%s ;"

    datos=(_nombre,_apellido,_correo,_materia,id)

    conn = mysql.connect()
    cursor=conn.cursor()

    now=datetime.now()
    tiempo=now.strftime("%Y%H%M%S")

    if _foto.filename!='':
    
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
        
        cursor.execute("SELECT Foto FROM maestros WHERE id=%s",id)
        fila=cursor.fetchall()

        os.remove(os.path.join(app.config ['CARPETA'],fila[0][0]))
        cursor.execute("UPDATE maestros SET foto=%s WHERE id=%s",(nuevoNombreFoto,id))
        conn.commit()

    cursor.execute(sql,datos)
    conn.commit()
    
    return redirect('/')

@app.route('/create')
def create():
    return render_template('maestros/create.html')


@app.route('/store', methods=['POST'])
def storage():

    _nombre=request.form['txtNombre']
    _apellido=request.form['txtApellido']
    _correo=request.form['txtCorreo']
    _materia=request.form['txtMateria']
    _foto=request.files['txtFoto']

    now=datetime.now()
    tiempo=now.strftime("%Y%H%M%S")

    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)


    sql= "INSERT INTO `maestros` (`Id`, `Nombre`, `Apellido`, `Correo`, `Materia`,`Foto`) VALUES (NULL,%s,%s,%s,%s,%s);"

    datos=(_nombre,_apellido,_correo,_materia,nuevoNombreFoto)

    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/')
    

if __name__ =='__main__':
    app.run(debug=True)