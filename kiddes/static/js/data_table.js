
$(document).ready(function() {
    if ($.fn.DataTable.isDataTable("#example2")) {
        $("#example2").DataTable().destroy();
    }

    var table = $('#example2').DataTable({
        lengthChange: false,
        dom: 'Bfrtip',  // Necesario para mostrar los botones
        buttons: ['copy', 'excel', 'pdf', 'print'],
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json"
        },
        initComplete: function() {
            console.log("Traducción cargada correctamente.");
        }
    });

    table.buttons().container()
        .appendTo('#example2_wrapper .col-md-6:eq(0)');
});

$(document).ready(function() {
    if ($.fn.DataTable.isDataTable("#productos")) {
        $("#productos").DataTable().destroy();
    }

    var table = $('#productos').DataTable({
        lengthChange: false,
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'copy',
                exportOptions: {
                    columns: ':visible',
                    format: {
                        body: function(data, row, column, node) {
                            if (column === 5) { // Columna de tallas
                                return $(node).text().replace(/\s+/g, ' ').trim();
                            }
                            if (column === 6) { // Columna de colores
                                return $(node).find('.color-circle').map(function() {
                                    return $(this).attr('data-color');
                                }).get().join(', ');
                            }
                            return data;
                        }
                    }
                }
            },
            {
                extend: 'excel',
                exportOptions: {
                    columns: ':visible',
                    format: {
                        body: function(data, row, column, node) {
                            if (column === 5) { // Columna de tallas
                                return $(node).text().replace(/\s+/g, ' ').trim();
                            }
                            if (column === 6) { // Columna de colores
                                return $(node).find('.color-circle').map(function() {
                                    return $(this).attr('data-color');
                                }).get().join(', ');
                            }
                            return data;
                        }
                    }
                }
            },
            {
                extend: 'pdf',
                exportOptions: {
                    columns: ':visible',
                    format: {
                        body: function(data, row, column, node) {
                            if (column === 5) { // Columna de tallas
                                return $(node).text().replace(/\s+/g, ' ').trim();
                            }
                            if (column === 6) { // Columna de colores
                                return $(node).find('.color-circle').map(function() {
                                    return $(this).attr('data-color');
                                }).get().join(', ');
                            }
                            return data;
                        }
                    }
                }
            },
            {
                extend: 'print',
                exportOptions: {
                    columns: ':visible',
                    format: {
                        body: function(data, row, column, node) {
                            if (column === 5) { // Columna de tallas
                                return $(node).text().replace(/\s+/g, ' ').trim();
                            }
                            if (column === 6) { // Columna de colores
                                return $(node).find('.color-circle').map(function() {
                                    return $(this).attr('data-color');
                                }).get().join(', ');
                            }
                            return data;
                        }
                    }
                }
            }
        ],
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json"
        },
        columnDefs: [
            { 
                targets: 5, // Columna de tallas
                orderable: true,
                searchable: true,
                render: function(data, type, row) {
                    return data.replace(/\s+/g, ' ').trim();
                }
            },
            { 
                targets: 6, // Columna de colores
                orderable: true, 
                searchable: true, 
                render: function(data, type, row, meta) {
                    if (type === 'filter' || type === 'sort') {
                        var tempDiv = document.createElement("div");
                        tempDiv.innerHTML = data;
                        return Array.from(tempDiv.querySelectorAll(".color-circle")).map(span => span.getAttribute("data-color")).join(', ');
                    }
                    return data;
                }
            }
        ],
        initComplete: function() {
            console.log("Traducción cargada correctamente.");
        }
    });

    table.buttons().container()
        .appendTo('#productos_wrapper .col-md-6:eq(0)');
});





