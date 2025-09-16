document.addEventListener('DOMContentLoaded', function() {
    
    // Auto-focus en el campo de usuario
    const usernameField = document.getElementById('username');
    if (usernameField) {
        usernameField.focus();
    }
    
    // Auto-hide mensajes flash despues de 5 segundos
    const flashMessages = document.querySelectorAll('.message_login');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });
    
    // Navegacion con Enter (usuario -> contraseña)
    if (usernameField) {
        usernameField.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const passwordField = document.getElementById('password');
                if (passwordField) {
                    passwordField.focus();
                }
            }
        });
    }
    
    // Estado de carga en el boton al enviar formulario
    const form = document.querySelector('.form_login');
    if (form) {
        form.addEventListener('submit', function() {
            const button = document.querySelector('.button_login');
            if (button) {
                button.disabled = true;
                button.classList.add('loading');
                button.textContent = 'Iniciando...';
            }
        });
    }
});