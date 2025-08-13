from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

# Configuración usando variables de entorno
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

# Inicializar Mail
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

@app.route("/nuestra_empresa")
def nuestra_empresa():
    return render_template("nuestra_empresa.html", active_page="nuestra empresa")

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
                recipients=['mauro.contreraspalma@gmail.com'],  # Tu email donde recibes mensajes
                body=body,
                reply_to=email
            )
            
            mail.send(msg)
            flash('¡Mensaje enviado correctamente! Te responderemos pronto.', 'success')
        except Exception as e:
            flash('Error al enviar el mensaje. Inténtalo de nuevo.', 'error')
        
        return redirect(url_for('contacto'))
    
    return render_template("contacto.html", active_page="contacto")

@app.route("/galeria")
def galeria():
    return render_template("galeria.html", active_page="galeria")

if __name__ == '__main__':
    app.run(debug=True)
