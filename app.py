from flask import Flask, render_template, request, flash, redirect, url_for
import os
from dotenv import load_dotenv
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Configuración SendGrid
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
FROM_EMAIL = os.environ.get('FROM_EMAIL')
TO_EMAIL = os.environ.get('TO_EMAIL')

sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

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

        subject = f"Nuevo mensaje de contacto de {nombre}"
        body_text = f"""
        Has recibido un nuevo mensaje desde tu sitio web:

        Nombre: {nombre}
        Email: {email}

        Mensaje:
        {mensaje}
        """

        try:
            # Crear y enviar email con SendGrid
            from_email = Email(FROM_EMAIL)
            to_email = To(TO_EMAIL)
            content = Content("text/plain", body_text)
            mail = Mail(from_email, to_email, subject, content)

            # Configurar reply_to
            mail.reply_to = Email(email)

            sg.client.mail.send.post(request_body=mail.get())

            flash('¡Mensaje enviado correctamente! Te responderemos pronto.', 'success')
        except Exception as e:
            print(f"Error al enviar email: {e}")
            flash('Error al enviar el mensaje. Inténtalo de nuevo.', 'error')

        return redirect(url_for('contacto'))

    return render_template("contacto.html", active_page="contacto")

@app.route("/galeria")
def galeria():
    return render_template("galeria.html", active_page="galeria")

if __name__ == '__main__':
    app.run(debug=True)
