from flask import Flask, render_template, request, flash, redirect, url_for, abort
import os
import re
import html
from datetime import datetime
from dotenv import load_dotenv
import sendgrid
from sendgrid.helpers.mail import Mail

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Headers de seguridad
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; script-src 'self' https://cdn.jsdelivr.net; img-src 'self' data: https:; font-src 'self' https://cdn.jsdelivr.net;"
    return response

# Configuración SendGrid
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
FROM_EMAIL = os.environ.get('FROM_EMAIL')
TO_EMAIL = os.environ.get('TO_EMAIL')

sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

# Funciones de validación y seguridad
def validate_input(text, max_length=1000):
    """Valida y limpia el input del usuario"""
    if not text or len(text.strip()) == 0:
        return None
    
    # Limitar longitud
    text = text[:max_length]
    
    # Escapar HTML para prevenir XSS
    text = html.escape(text.strip())
    
    return text

def is_valid_email(email):
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def detect_spam_patterns(text):
    """Detecta patrones comunes de spam"""
    spam_keywords = ['viagra', 'casino', 'lottery', 'winner', 'urgent', 'million dollars', 'click here', 'free money']
    text_lower = text.lower()
    
    # Verificar palabras spam
    for keyword in spam_keywords:
        if keyword in text_lower:
            return True
    
    # Verificar exceso de enlaces
    url_count = len(re.findall(r'http[s]?://', text_lower))
    if url_count > 2:
        return True
    
    # Verificar caracteres repetidos (indicativo de spam)
    if len(re.findall(r'(.)\1{4,}', text_lower)) > 0:
        return True
    
    return False

def get_client_ip():
    """Obtiene la IP real del cliente"""
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']

# Control básico de rate limiting (en memoria)
recent_submissions = {}

def is_rate_limited(ip_address, max_requests=3, time_window=300):  # 3 requests per 5 minutes
    """Verifica si una IP está enviando demasiados requests"""
    current_time = datetime.now().timestamp()
    
    if ip_address not in recent_submissions:
        recent_submissions[ip_address] = []
    
    # Limpiar submissions antiguas
    recent_submissions[ip_address] = [
        timestamp for timestamp in recent_submissions[ip_address]
        if current_time - timestamp < time_window
    ]
    
    # Verificar límite
    if len(recent_submissions[ip_address]) >= max_requests:
        return True
    
    # Agregar nueva submission
    recent_submissions[ip_address].append(current_time)
    return False

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
        # Verificar rate limiting
        client_ip = get_client_ip()
        if is_rate_limited(client_ip):
            flash('Demasiadas solicitudes. Por favor espera unos minutos antes de enviar otro mensaje.', 'error')
            return redirect(url_for('contacto'))
        
        # Obtener y validar datos del formulario
        nombre = validate_input(request.form.get('nombre', ''), 50)
        email = validate_input(request.form.get('email', ''), 100)
        mensaje = validate_input(request.form.get('mensaje', ''), 1000)
        
        # Validaciones de seguridad
        if not all([nombre, email, mensaje]):
            flash('Todos los campos son requeridos.', 'error')
            return redirect(url_for('contacto'))
        
        if len(nombre) < 2:
            flash('El nombre debe tener al menos 2 caracteres.', 'error')
            return redirect(url_for('contacto'))
        
        if not is_valid_email(email):
            flash('Por favor ingresa un email válido.', 'error')
            return redirect(url_for('contacto'))
        
        if len(mensaje) < 10:
            flash('El mensaje debe tener al menos 10 caracteres.', 'error')
            return redirect(url_for('contacto'))
        
        if detect_spam_patterns(mensaje) or detect_spam_patterns(nombre):
            flash('Tu mensaje ha sido marcado como spam. Por favor revisa el contenido.', 'error')
            return redirect(url_for('contacto'))

        subject = f"Nuevo mensaje de contacto de {nombre}"

        try:
            # Crear y enviar email con SendGrid (método simplificado)
            message = Mail(
                from_email=FROM_EMAIL,
                to_emails=TO_EMAIL,
                subject=subject,
                html_content=f'''
                <h2>🌍 Nuevo mensaje de contacto desde tu sitio web</h2>
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 10px 0;">
                    <p><strong>👤 Nombre:</strong> {nombre}</p>
                    <p><strong>📧 Email:</strong> {email}</p>
                    <p><strong>📅 Fecha:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                    <p><strong>🌐 IP del remitente:</strong> {client_ip}</p>
                </div>
                <div style="background-color: #ffffff; padding: 20px; border-left: 4px solid #007bff; margin: 10px 0;">
                    <p><strong>💬 Mensaje:</strong></p>
                    <p style="font-style: italic;">{mensaje.replace(chr(10), '<br>')}</p>
                </div>
                <hr style="margin: 20px 0;">
                <p style="font-size: 12px; color: #666;">
                    <small>🔒 Este mensaje fue enviado desde el formulario de contacto seguro de tu sitio web de viajes.</small>
                </p>
                '''
            )
            
            # Configurar reply-to
            message.reply_to = email
            
            # Enviar el email
            response = sg.send(message)
            
            # Verificar que el email fue enviado exitosamente
            if response.status_code in [200, 201, 202]:
                print(f"✅ Email enviado exitosamente. Status: {response.status_code} - IP: {client_ip}")
                flash('¡Mensaje enviado correctamente! Te responderemos pronto.', 'success')
            else:
                print(f"❌ Error en el envío. Status: {response.status_code} - IP: {client_ip}")
                flash('Error al enviar el mensaje. Inténtalo de nuevo.', 'error')

        except Exception as e:
            print(f"❌ Error al enviar email: {e} - IP: {client_ip}")
            print(f"Tipo de error: {type(e).__name__}")
            flash('Error al enviar el mensaje. Inténtalo de nuevo.', 'error')

        return redirect(url_for('contacto'))

    return render_template("contacto.html", active_page="contacto")

@app.route("/galeria")
def galeria():
    return render_template("galeria.html", active_page="galeria")

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Para desarrollo local
    app.run(debug=True)
else:
    # Para producción (Render)
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
