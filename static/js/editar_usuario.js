document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form-usuario-editar");
    const username = document.getElementById("username");
    const email = document.getElementById("email");
    const nombre = document.getElementById("nombre");
    const apellido = document.getElementById("apellido");
    const rol = document.getElementById("rol");
    const password = document.getElementById("password");

    form.addEventListener("submit", function (e) {
        let errores = [];

        if (!username.value.trim()) errores.push("El usuario es obligatorio");
        else if (username.value.length < 3 || username.value.length > 50)
            errores.push("El usuario debe tener entre 3 y 50 caracteres");

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!email.value.trim()) errores.push("El email es obligatorio");
        else if (!emailRegex.test(email.value)) errores.push("Formato de email invalido");

        const nombreRegex = /^[A-Za-zaeiouaeiouÑñ\s]+$/;
        if (!nombre.value.trim()) errores.push("El nombre es obligatorio");
        else if (!nombreRegex.test(nombre.value)) errores.push("El nombre solo puede contener letras");

        if (apellido.value && !nombreRegex.test(apellido.value))
            errores.push("El apellido solo puede contener letras");

        const rolesValidos = ["admin", "usuario", "supervisor"];
        if (!rolesValidos.includes(rol.value))
            errores.push("El rol seleccionado no es valido");

        if (errores.length > 0) {
            e.preventDefault();
            alert(errores.join("\n"));
        }
    });
});
