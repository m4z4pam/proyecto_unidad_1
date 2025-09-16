document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("productoForm");
    const errorContainer = document.getElementById("errores");

    form.addEventListener("submit", (event) => {
        let errores = [];

        const nombre = document.getElementById("nombre").value.trim();
        const categoria = document.getElementById("categoria").value.trim();
        const precio = parseFloat(document.getElementById("precio").value);
        const stock = parseInt(document.getElementById("stock").value);
        const costo = parseFloat(document.getElementById("costo").value);

        const regexNombre = /^[a-zA-ZaeiouÑaeiouñ\s]{3,100}$/; 
        if (!regexNombre.test(nombre)) {
            errores.push("El nombre solo debe contener letras y espacios (minimo 3 caracteres, maximo 100).");
        }

        const categoriasValidas = ["Escolares", "Oficina", "Arte"];
        if (!categoriasValidas.includes(categoria)) {
            errores.push("Selecciona una categoria valida.");
        }

        if (isNaN(precio) || precio <= 0) {
            errores.push("El precio debe ser un numero mayor a 0.");
        }

        if (isNaN(stock) || stock < 0) {
            errores.push("El stock debe ser un numero mayor o igual a 0.");
        }

        if (isNaN(costo) || costo < 0) {
            errores.push("El costo debe ser un numero mayor o igual a 0.");
        }

        if (!isNaN(precio) && !isNaN(costo) && costo > precio) {
            errores.push("El costo no puede ser mayor que el precio de venta.");
        }

        if (errores.length > 0) {
            event.preventDefault();

            if (errorContainer) {
                errorContainer.innerHTML = errores.map(err => `<p class="error">${err}</p>`).join("");
            } else {
                alert(errores.join("\n"));
            }
        }
    });
});
