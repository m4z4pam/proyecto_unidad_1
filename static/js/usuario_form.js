document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("usuario_form"); 
    const username = document.getElementById("username");
    const email = document.getElementById("email");
    const password = document.getElementById("password");
    const nombre = document.getElementById("nombre");
    const apellido = document.getElementById("apellido");
    const rol = document.getElementById("rol");

    form.addEventListener("submit", function (e) {
        let errores = [];

        if (!username.value.trim()) {
            errores.push("El usuario es obligatorio");
        } else if (username.value.length < 3 || username.value.length > 50) {
            errores.push("El usuario debe tener entre 3 y 50 caracteres");
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!email.value.trim()) {
            errores.push("El email es obligatorio");
        } else if (!emailRegex.test(email.value)) {
            errores.push("El formato de email es invalido");
        }

        if (password) {
            if (!password.value.trim()) {
                errores.push("La contraseña es obligatoria");
            } else if (password.value.length < 6) {
                errores.push("La contraseña debe tener al menos 6 caracteres");
            }
        }

        if (!nombre.value.trim()) {
            errores.push("El nombre es obligatorio");
        } else if (nombre.value.length < 2 || nombre.value.length > 100) {
            errores.push("El nombre debe tener entre 2 y 100 caracteres");
        }

        if (apellido.value && apellido.value.length > 100) {
            errores.push("El apellido no puede exceder 100 caracteres");
        }

        const rolesValidos = ["admin", "usuario", "supervisor"];
        if (!rolesValidos.includes(rol.value)) {
            errores.push("El rol seleccionado no es valido");
        }

        if (errores.length > 0) {
            e.preventDefault();
            alert(errores.join("\n"));
        }
    });
});
