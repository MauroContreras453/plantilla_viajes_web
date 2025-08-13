// Animación suave al hacer scroll a enlaces internos
document.querySelectorAll('a[href^="#"]').forEach(enlace => {
    enlace.addEventListener("click", function(e) {
        e.preventDefault();
        const destino = document.querySelector(this.getAttribute("href"));
        if (destino) {
            destino.scrollIntoView({
                behavior: "smooth"
            });
        }
    });
});

// Validación básica del formulario de contacto
document.addEventListener("DOMContentLoaded", () => {
    const formulario = document.querySelector("form");

    if (formulario) {
        formulario.addEventListener("submit", (e) => {
            e.preventDefault(); // Evita envío automático para validar primero

            const nombre = formulario.querySelector('input[type="text"]').value.trim();
            const correo = formulario.querySelector('input[type="email"]').value.trim();
            const mensaje = formulario.querySelector('textarea').value.trim();

            if (nombre.length < 3) {
                alert("Por favor ingresa un nombre válido (mínimo 3 caracteres).");
                return;
            }
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo)) {
                alert("Por favor ingresa un correo electrónico válido.");
                return;
            }
            if (mensaje.length < 10) {
                alert("El mensaje debe tener al menos 10 caracteres.");
                return;
            }

            // Si pasa todas las validaciones
            alert("¡Gracias por contactarnos! Te responderemos pronto.");
            formulario.reset();
        });
    }

    // Lógica para galería de imágenes
    document.querySelectorAll('.gallery-img').forEach(img => {
        img.addEventListener('click', () => {
            const modalImg = document.getElementById('imagenModal');
            if (modalImg) {
                modalImg.src = img.src;
                new bootstrap.Modal(document.getElementById('modalImagen')).show();
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", () => {

    // Función genérica para manejar formularios con SweetAlert2
    async function manejarFormulario(formularioId) {
        const formulario = document.getElementById(formularioId);
        if (!formulario) return;

        formulario.addEventListener("submit", async (e) => {
            e.preventDefault();

            const formData = new FormData(formulario);

            try {
                const response = await fetch(formulario.action || window.location.pathname, {
                    method: "POST",
                    body: formData
                });

                if (response.ok) {
                    Swal.fire({
                        icon: 'success',
                        title: '¡Mensaje enviado!',
                        text: 'Te responderemos pronto.',
                        confirmButtonColor: '#007bff'
                    });
                    formulario.reset();
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'No se pudo enviar el mensaje. Intenta nuevamente.',
                        confirmButtonColor: '#dc3545'
                    });
                }
            } catch (error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Hubo un problema al enviar el mensaje.',
                    confirmButtonColor: '#dc3545'
                });
            }
        });
    }

    // Manejar el formulario de contacto general
    manejarFormulario("form-contacto");

    // Manejar el formulario de "Trabaja con nosotros"
    manejarFormulario("form-contacto-empresa");
});

