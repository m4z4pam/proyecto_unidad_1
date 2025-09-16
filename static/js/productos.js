document.addEventListener("DOMContentLoaded", function() {
    const inputBusqueda = document.getElementById("busquedaNombre");

    if (inputBusqueda) {
        let timeout = null;
        inputBusqueda.addEventListener("input", function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                const valor = inputBusqueda.value.trim();
                if (valor.length > 0) {
                    window.location.href = "/productos/buscar?q=" + encodeURIComponent(valor);
                } else {
                    window.location.href = "/productos";
                }
            }, 500); // medio segundo de espera
        });
    }
});
