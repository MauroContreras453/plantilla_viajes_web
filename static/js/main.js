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
            const nombre = formulario.querySelector('input[name="nombre"]').value.trim();
            const correo = formulario.querySelector('input[name="email"]').value.trim();
            const mensaje = formulario.querySelector('textarea[name="mensaje"]').value.trim();

            if (nombre.length < 3) {
                e.preventDefault();
                alert("Por favor ingresa un nombre válido (mínimo 3 caracteres).");
                return;
            }
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo)) {
                e.preventDefault();
                alert("Por favor ingresa un correo electrónico válido.");
                return;
            }
            if (mensaje.length < 10) {
                e.preventDefault();
                alert("El mensaje debe tener al menos 10 caracteres.");
                return;
            }

            // Si pasa todas las validaciones, permite el envío normal del formulario
            // No llamamos preventDefault() ni reset() para que Flask maneje el envío
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

