document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("clienteForm");


    form.addEventListener("submit", function (event) {

        let nombre = document.getElementById("nombre").value.trim();
        let telefono = document.getElementById("telefono").value.trim();
        let email = document.getElementById("email").value.trim();

        console.log("Validando:", { nombre, telefono, email });

        if (nombre === "") {
            alert("El nombre es obligatorio");
            event.preventDefault();
            return;
        }

        if (telefono.length > 10 || telefono && !/^\d+$/.test(telefono) || telefono.length < 10) {
            alert("El telefono solo debe contener numeros, y un maximo de 10 digitos");
            event.preventDefault();
            return;
        }

        if (email && !/^[\w-.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email) || email.length > 100 || !email) {
            alert("El correo no es valido");
            event.preventDefault();
            return;
        }

    });
});
