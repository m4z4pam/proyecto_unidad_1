document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("proveedorForm");

    form.addEventListener("submit", (e) => {
        let errores = [];

        const nombre = document.getElementById("nombre").value.trim();
        const rfc = document.getElementById("rfc").value.trim();
        const telefono = document.getElementById("telefono").value.trim();
        const email = document.getElementById("email").value.trim();
        const direccion = document.getElementById("direccion").value.trim();

        if (!nombre) {
            errores.push("El nombre es obligatorio.");
        }
        const regexRFC = /^[A-ZÑ&]{3}\d{6}[A-Z0-9]{3}$/;
        if (!regexRFC.test(rfc)) {
            errores.push("El RFC ingresado no es valido.");
        }
        if (telefono.length > 10 || telefono && !/^\d+$/.test(telefono) || telefono.length < 10) {
            errores.push("El telefono solo debe ser un numero real telefonico y no puede superar 20 caracteres.");
        }
        if (email && !/^[\w-.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email) || email.length > 100 || !email) {
            errores.push("El email no es valido.");
        }
        if (direccion.length > 150) {
            errores.push("La direccion no puede superar 150 caracteres.");
        }
        if (errores.length > 0) {
            e.preventDefault();
            alert("Errores:\n- " + errores.join("\n- "));
        }
    });
});
