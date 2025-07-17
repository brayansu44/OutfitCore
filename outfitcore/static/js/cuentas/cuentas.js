function ViewDelete(aux, id, auxi) {
    Swal.fire({
        title: `¿Deseas eliminar esta ${auxi}?`,
        text: "Una vez eliminada, no podrás recuperarla.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/cuentas/${aux}/facturas/delete/${id}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        Swal.fire("Eliminado", `La ${auxi} ha sido eliminada.`, "success")
                            .then(() => location.reload());
                    } else {
                        Swal.fire("Error", `No se pudo eliminar la ${auxi}.`, "error");
                    }
                })
                .catch(error => {
                    Swal.fire("Error", "Hubo un problema con la solicitud.", "error");
                });
        }
    });
}

// FORM AGREGAR CLIENTE
document.addEventListener("DOMContentLoaded", function () {

    // FACTURA DE VENTA

    let clienteFormURL = "";
    // Cargar el formulario cuando se abre el modal
    $('#modalCliente').on('show.bs.modal', function (event) {
        const trigger  = $(event.relatedTarget);
        clienteFormURL = trigger.data('url');  // ← captura la URL definida en el HTML
        $('#modalClienteBody').html(`
            <div class="text-center py-4">
                <div class="spinner-border text-primary" role="status"></div>
                <p class="mt-2">Cargando formulario...</p>
            </div>
        `);

        $.get(clienteFormURL, function (data) {
            $('#modalClienteBody').html(data);
        });
    });

    // Enviar el formulario via AJAX
    $(document).on('submit', '#clienteForm', function (e) {
        e.preventDefault();
        $.post(clienteFormURL, $(this).serialize(), function (data) {
            if (data.success) {
                let nuevaOpcion = new Option(data.nombre, data.id, true, true);
                $('#id_cliente').append(nuevaOpcion).trigger('change');
                $('#modalCliente').modal('hide');
            } else {
                $('#modalClienteBody').html(data.form_html);
            }
        });
    })

    
    document.querySelectorAll(".delete-factura").forEach(button => {
        button.addEventListener("click", function () {
            let aux = this.id;
            let id = this.getAttribute("data-id")
            let auxi = "factura"
            
            ViewDelete(aux, id, auxi)

        });
    });

    // PAGO DE VENTA
    
    let facturaFormURL = "";
    // Cargar el formulario cuando se abre el modal
    $('#modalFactura').on('show.bs.modal', function (event) {
        const trigger  = $(event.relatedTarget);
        facturaFormURL = trigger.data('url');  // ← captura la URL definida en el HTML
        $('#modalFacturaBody').html(`
            <div class="text-center py-4">
                <div class="spinner-border text-primary" role="status"></div>
                <p class="mt-2">Cargando formulario...</p>
            </div>
        `);

        $.get(facturaFormURL, function (data) {
            $('#modalFacturaBody').html(data);
        });
    });

    // Enviar el formulario via AJAX
    $(document).on('submit', '#facturaForm', function (e) {
        e.preventDefault();
        $.post(facturaFormURL, $(this).serialize(), function (data) {
            if (data.success) {
                let nuevaOpcion = new Option(data.nombre, data.id, true, true);
                $('#id_cliente').append(nuevaOpcion).trigger('change');
                $('#modalFactura').modal('hide');
            } else {
                $('#modalFacturaBody').html(data.form_html);
            }
        });
    })

    
    document.querySelectorAll(".delete-pago").forEach(button => {
        button.addEventListener("click", function () {
            let aux = this.id;
            let id = this.getAttribute("data-id")
            let auxi = "pago"
            
            ViewDelete(aux, id, auxi)

        });
    });

});


$(document).ready(function () {

    (function () {
        'use strict';
        var forms = document.querySelectorAll('.needs-validation');
        Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    })();

});