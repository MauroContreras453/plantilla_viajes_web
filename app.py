from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
import os

app = Flask(__name__, instance_relative_config=True)

# Cargar la configuración desde instance/config.py
app.config.from_pyfile('config.py')

mail = Mail(app)

@app.route("/")
def index():
    return render_template("index.html", active_page="inicio")

@app.route("/destinos")
def destinos():
    return render_template("destinos.html", active_page="destinos")

@app.route("/consejos")
def consejos():
    return render_template("consejos.html", active_page="consejos")

@app.route("/contacto", methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        mensaje = request.form['mensaje']
        
        # Crear el mensaje de email
        subject = f"Nuevo mensaje de contacto de {nombre}"
        body = f"""
        Has recibido un nuevo mensaje desde tu sitio web:
        
        Nombre: {nombre}
        Email: {email}
        
        Mensaje:
        {mensaje}
        """
        
        try:
            # Crear y enviar el email
            msg = Message(
                subject=subject,
                recipients=['ejemplo@gmail.com'],
                body=body,
                reply_to=email
            )
            mail.send(msg)
            flash('¡Mensaje enviado correctamente! Te responderemos pronto.', 'success')
        except Exception as e:
            flash('Error al enviar el mensaje. Inténtalo de nuevo.', 'error')
            print(f"Error: {e}")
        
        return redirect(url_for('contacto'))
    
    return render_template("contacto.html", active_page="contacto")

@app.route("/galeria")
def galeria():
    return render_template("galeria.html", active_page="galeria")

if __name__ == '__main__':
    app.run(debug=True)
