document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("password_form");
    const nueva = document.getElementById("nueva_password");
    const confirmar = document.getElementById("confirmar_password");

    form.addEventListener("submit", function (e) {
        let errores = [];

        if (!nueva.value.trim()) {
            errores.push("La nueva contraseña es requerida");
        } else if (nueva.value.length < 6) {
            errores.push("La contraseña debe tener al menos 6 caracteres");
        }

        if (!confirmar.value.trim()) {
            errores.push("Debe confirmar la nueva contraseña");
        } else if (confirmar.value !== nueva.value) {
            errores.push("Las contraseñas no coinciden");
        }

        if (errores.length > 0) {
            e.preventDefault();
            alert(errores.join("\n"));
        }
    });
});
