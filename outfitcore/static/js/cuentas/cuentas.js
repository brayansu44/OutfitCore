function ViewDelete(url, aux, id) {
    Swal.fire({
        title: `¿Deseas eliminar esta ${aux}?`,
        text: "Una vez eliminada, no podrás recuperarla.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/cuentas/${url}/${aux}s/delete/${id}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        Swal.fire("Eliminado", `La ${aux} ha sido eliminada.`, "success")
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

// VIEW DELETE
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-factura").forEach(button => {
        button.addEventListener("click", function () {
            let url = this.id
            let aux = "factura"
            let id = this.getAttribute("data-id")
            
            ViewDelete(url, aux, id)

        });
    });

    document.querySelectorAll(".delete-pago").forEach(button => {
        button.addEventListener("click", function () {
            let url = this.id
            let aux = "pago"
            let id = this.getAttribute("data-id")
            
            ViewDelete(url, aux, id)

        });
    });

})
// FORM "AGREGAR" MODAL
document.addEventListener("DOMContentLoaded", function () {

    // FACTURA DE VENTA - MODAL CLIENTE

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

    //Lanzar SUBMIT del FORM
    $(document).on('click', '#submitAddCliente', function () {
        const form = document.getElementById('clienteForm');
        if (form.checkValidity()) {
            $('#clienteForm').submit();
        } else {
            form.reportValidity();  // muestra los errores nativos del navegador
        }
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

    
    
    // PAGO DE VENTA - MODAL FACTURA
    
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

    //Lanzar SUBMIT del FORM
    $(document).on('click', '#submitAddFactura', function () {
        const form = document.getElementById('facturaForm');
        if (form.checkValidity()) {
            $('#facturaForm').submit();
        } else {
            form.reportValidity();  // muestra los errores nativos del navegador
        }
    });

    // Enviar el formulario via AJAX
    $(document).on('submit', '#facturaForm', function (e) {
        e.preventDefault();
        $.post(facturaFormURL, $(this).serialize(), function (data) {
            if (data.success) {
                let nuevaOpcion = new Option(data.numero_factura, data.id, true, true);
                $('#id_factura').append(nuevaOpcion).trigger('change');
                $('#modalFactura').modal('hide');
            } else {
                $('#modalFacturaBody').html(data.form_html);
            }
        });
    })

    // PAGO DE VENTA - MODAL FACTURA COMPRA
    
    let facturaCompraFormURL = "";
    // Cargar el formulario cuando se abre el modal
    $('#modalFacturaCompra').on('show.bs.modal', function (event) {
        const trigger  = $(event.relatedTarget);
        facturaCompraFormURL = trigger.data('url');  // ← captura la URL definida en el HTML
        $('#modalFacturaCompraBody').html(`
            <div class="text-center py-4">
                <div class="spinner-border text-primary" role="status"></div>
                <p class="mt-2">Cargando formulario...</p>
            </div>
        `);

        $.get(facturaCompraFormURL, function (data) {
            $('#modalFacturaCompraBody').html(data);
        });
    });

    //Lanzar SUBMIT del FORM
    $(document).on('click', '#submitAddFacturaCompra', function () {
        const form = document.getElementById('facturaCompraForm');
        if (form.checkValidity()) {
            $('#facturaCompraForm').submit();
        } else {
            form.reportValidity();  // muestra los errores nativos del navegador
        }
    });

    // Enviar el formulario via AJAX
    $(document).on('submit', '#facturaCompraForm', function (e) {
        e.preventDefault();
        $.post(facturaCompraFormURL, $(this).serialize(), function (data) {
            if (data.success) {
                let nuevaOpcion = new Option(data.numero_factura, data.id, true, true);
                $('#id_factura').append(nuevaOpcion).trigger('change');
                $('#modalFacturaCompra').modal('hide');
            } else {
                $('#modalFacturaCompraBody').html(data.form_html);
            }
        });
    })
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