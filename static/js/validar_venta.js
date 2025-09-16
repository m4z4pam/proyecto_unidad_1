document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("ventaForm");
    const clienteSelect = document.getElementById("id_cliente");
    const cantidades = document.querySelectorAll(".cantidad");

    form.addEventListener("submit", (event) => {
        let errores = [];

        if (!clienteSelect.value) {
            errores.push("Debes seleccionar un cliente.");
        }

        let totalSeleccionados = 0;
        cantidades.forEach(campo => {
            const cantidad = parseInt(campo.value) || 0;
            const maxStock = parseInt(campo.getAttribute("max"));

            if (cantidad > 0) {
                totalSeleccionados++;
                if (cantidad > maxStock) {
                    errores.push(`La cantidad de "${campo.closest("tr").cells[0].textContent}" excede el stock disponible (${maxStock}).`);
                }
            }
        });

        if (totalSeleccionados === 0) {
            errores.push("Debes seleccionar al menos un producto con cantidad mayor a 0.");
        }

        if (errores.length > 0) {
            alert(errores.join("\n"));
            event.preventDefault();
        }
    });
});
