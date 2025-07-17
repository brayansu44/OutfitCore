// FORM AGREGAR CLIENTE
document.addEventListener("DOMContentLoaded", function () {
    // Cargar el formulario cuando se abre el modal
    $('#modalCliente').on('show.bs.modal', function () {

        $('#modalClienteBody').html(`
            <div id="spinnerCliente" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Cargando...</span>
                </div>
                <p class="mt-2">Cargando formulario...</p>
            </div>
        `);

        $.get("{% url 'agregar_cliente' %}", function (data) {
            $('#modalClienteBody').html(data);
        });
    });

    // Enviar el formulario via AJAX
    $('#clienteForm').submit(function (e) {
        e.preventDefault();
        $.post("{% url 'agregar_cliente' %}", $(this).serialize(), function (data) {
            if (data.success) {
                // Agregar cliente al select y seleccionar automáticamente
                let nuevaOpcion = new Option(data.nombre, data.id, true, true);
                $('#id_cliente').append(nuevaOpcion).trigger('change');
                $('#modalCliente').modal('hide');
            } else {
                $('#modalClienteBody').html(data.form_html);
            }
        });
    });
});

