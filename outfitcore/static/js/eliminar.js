
//Telas

const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-tela").forEach(button => {
        button.addEventListener("click", function () {
            let telaId = this.getAttribute("data-id");

            Swal.fire({
                title: "¿Deseas eliminar esta tela?",
                text: "Una vez eliminada, no podrás recuperarla.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                cancelButtonColor: "#3085d6",
                confirmButtonText: "Sí, eliminar",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`/trazabilidad/telas/eliminar/${telaId}/`, {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": csrfToken
                        }
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                Swal.fire("Eliminado", "La tela ha sido eliminada.", "success")
                                    .then(() => location.reload());
                            } else {
                                Swal.fire("Error", "No se pudo eliminar la tela.", "error");
                            }
                        })
                        .catch(error => {
                            Swal.fire("Error", "Hubo un problema con la solicitud.", "error");
                        });
                }
            });
        });
    });
});

// rollos
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-rollo").forEach(button => {
        button.addEventListener("click", function () {
            let rolloId = this.getAttribute("data-id");

            Swal.fire({
                title: "¿Deseas eliminar este rollo?",
                text: "Una vez eliminado, no podrás recuperarlo.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                cancelButtonColor: "#3085d6",
                confirmButtonText: "Sí, eliminar",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`/trazabilidad/rollos/eliminar/${rolloId}/`, {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": csrfToken
                        }
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                Swal.fire("Eliminado", "El rollo ha sido eliminado.", "success")
                                    .then(() => location.reload());
                            } else {
                                Swal.fire("Error", "No se pudo eliminar el rollo.", "error");
                            }
                        })
                        .catch(error => {
                            Swal.fire("Error", "Hubo un problema con la solicitud.", "error");
                        });
                }
            });
        });
    });
});

// ordenes
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-orden").forEach(button => {
        button.addEventListener("click", function () {
            let ordenId = this.getAttribute("data-id");

            Swal.fire({
                title: "¿Deseas eliminar esta orden?",
                text: "Una vez eliminado, no podrás recuperarla.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                cancelButtonColor: "#3085d6",
                confirmButtonText: "Sí, eliminar",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`/trazabilidad/ordenes_produccion/eliminar/${ordenId}/`, {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": csrfToken
                        }
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                Swal.fire("Eliminado", "La orden ha sido eliminada.", "success")
                                    .then(() => location.reload());
                            } else {
                                Swal.fire("Error", "No se pudo eliminar la orden.", "error");
                            }
                        })
                        .catch(error => {
                            Swal.fire("Error", "Hubo un problema con la solicitud.", "error");
                        });
                }
            });
        });
    });
});

// cortes
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-corte").forEach(button => {
        button.addEventListener("click", function () {
            let corteId = this.getAttribute("data-id");

            Swal.fire({
                title: "¿Deseas eliminar este corte?",
                text: "Una vez eliminado, no podrás recuperarlo.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                cancelButtonColor: "#3085d6",
                confirmButtonText: "Sí, eliminar",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`/trazabilidad/cortes/eliminar/${corteId}/`, {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": csrfToken
                        }
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                Swal.fire("Eliminado", "El corte ha sido eliminado.", "success")
                                    .then(() => location.reload());
                            } else {
                                Swal.fire("Error", "No se pudo eliminar el corte.", "error");
                            }
                        })
                        .catch(error => {
                            Swal.fire("Error", "Hubo un problema con la solicitud.", "error");
                        });
                }
            });
        });
    });
});


// tallas
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-talla").forEach(button => {
        button.addEventListener("click", function () {
            let tallaId = this.getAttribute("data-id");

            Swal.fire({
                title: "¿Deseas eliminar esta talla?",
                text: "Una vez eliminada, no podrás recuperarla.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                cancelButtonColor: "#3085d6",
                confirmButtonText: "Sí, eliminar",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`/trazabilidad/tallas_corte/eliminar/${tallaId}/`, {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": csrfToken
                        }
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                Swal.fire("Eliminado", "La talla ha sido eliminada.", "success")
                                    .then(() => location.reload());
                            } else {
                                Swal.fire("Error", "No se pudo eliminar la talla.", "error");
                            }
                        })
                        .catch(error => {
                            Swal.fire("Error", "Hubo un problema con la solicitud.", "error");
                        });
                }
            });
        });
    });
});


// retazos
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-retazo").forEach(button => {
        button.addEventListener("click", function () {
            let retazoId = this.getAttribute("data-id");

            Swal.fire({
                title: "¿Deseas eliminar este retazo?",
                text: "Una vez eliminado, no podrás recuperarlo.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                cancelButtonColor: "#3085d6",
                confirmButtonText: "Sí, eliminar",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`/trazabilidad/retazos_tela/eliminar/${retazoId}/`, {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": csrfToken
                        }
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                Swal.fire("Eliminado", "El retazo ha sido eliminado.", "success")
                                    .then(() => location.reload());
                            } else {
                                Swal.fire("Error", "No se pudo eliminar el retazo.", "error");
                            }
                        })
                        .catch(error => {
                            Swal.fire("Error", "Hubo un problema con la solicitud.", "error");
                        });
                }
            });
        });
    });
});

// productos
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-producto").forEach(button => {
        button.addEventListener("click", function () {
            let productoId = this.getAttribute("data-id");

            Swal.fire({
                title: "¿Deseas eliminar este producto?",
                text: "Una vez eliminado, no podrás recuperarlo.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                cancelButtonColor: "#3085d6",
                confirmButtonText: "Sí, eliminar",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`/productos/eliminar/${productoId}/`, {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": csrfToken
                        }
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                Swal.fire("Eliminado", "El producto ha sido eliminado.", "success")
                                    .then(() => location.reload());
                            } else {
                                Swal.fire("Error", "No se pudo eliminar el producto.", "error");
                            }
                        })
                        .catch(error => {
                            Swal.fire("Error", "Hubo un problema con la solicitud.", "error");
                        });
                }
            });
        });
    });
});

//locales
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-local").forEach(button => {
        button.addEventListener("click", function () {
            let localId = this.getAttribute("data-id");

            Swal.fire({
                title: "¿Deseas eliminar este local?",
                text: "Una vez eliminado, no podrás recuperarlo.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                cancelButtonColor: "#3085d6",
                confirmButtonText: "Sí, eliminar",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`/locales/eliminar/${localId}/`, {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": csrfToken
                        }
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                Swal.fire("Eliminado", "El local ha sido eliminado.", "success")
                                    .then(() => location.reload());
                            } else {
                                Swal.fire("Error", "No se pudo eliminar el local.", "error");
                            }
                        })
                        .catch(error => {
                            Swal.fire("Error", "Hubo un problema con la solicitud.", "error");
                        });
                }
            });
        });
    });
});

//Inventario local
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-inventario").forEach(button => {
        button.addEventListener("click", function () {
            let inventarioId = this.getAttribute("data-id");

            Swal.fire({
                title: "¿Deseas eliminar este inventario?",
                text: "Una vez eliminado, no podrás recuperarlo.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                cancelButtonColor: "#3085d6",
                confirmButtonText: "Sí, eliminar",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`/locales/inventario/eliminar/${inventarioId}/`, {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": csrfToken
                        }
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                Swal.fire("Eliminado", "El inventario ha sido eliminado.", "success")
                                    .then(() => location.reload());
                            } else {
                                Swal.fire("Error", "No se pudo eliminar el inventario.", "error");
                            }
                        })
                        .catch(error => {
                            Swal.fire("Error", "Hubo un problema con la solicitud.", "error");
                        });
                }
            });
        });
    });
});

// Bodega
document.addEventListener("DOMContentLoaded", function () {
    // Obtener el token CSRF del meta tag en base.html
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // Asociar eventos a todos los botones de eliminación
    document.querySelectorAll(".delete-salida").forEach(button => {
        button.addEventListener("click", function () {
            const salidaId = this.getAttribute("data-id");

            Swal.fire({
                title: "¿Qué deseas hacer?",
                text: "Puedes eliminar definitivamente o eliminar y devolver al stock de bodega.",
                icon: "warning",
                showCancelButton: true,
                showDenyButton: true,
                confirmButtonColor: "#198754",
                denyButtonColor: "#d33",
                cancelButtonColor: "#6c757d",
                confirmButtonText: "Eliminar y devolver",
                denyButtonText: "Eliminar definitivamente",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed || result.isDenied) {
                    const devolver = result.isConfirmed;

                    fetch(`/bodega/salidas/eliminar/${salidaId}/`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": csrfToken
                        },
                        body: JSON.stringify({ devolver: devolver })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            Swal.fire("Éxito", data.message || "Salida eliminada.", "success")
                                .then(() => location.reload());
                        } else {
                            Swal.fire("Error", data.error || "No se pudo eliminar la salida.", "error");
                        }
                    })
                    .catch(() => {
                        Swal.fire("Error", "Hubo un problema en la solicitud al servidor.", "error");
                    });
                }
            });
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-stock").forEach(button => {
        button.addEventListener("click", function () {
            let stockId = this.getAttribute("data-id");

            Swal.fire({
                title: "¿Deseas eliminar este stock?",
                text: "Una vez eliminado, no podrás recuperarlo.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                cancelButtonColor: "#3085d6",
                confirmButtonText: "Sí, eliminar",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`/bodega/inventario/eliminar/${stockId}/`, {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": csrfToken
                        }
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                Swal.fire("Eliminado", "El stock ha sido eliminado.", "success")
                                    .then(() => location.reload());
                            } else {
                                Swal.fire("Error", "No se pudo eliminar el stock.", "error");
                            }
                        })
                        .catch(error => {
                            Swal.fire("Error", "Hubo un problema con la solicitud.", "error");
                        });
                }
            });
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-entrada").forEach(button => {
        button.addEventListener("click", function () {
            let entradaId = this.getAttribute("data-id");

            Swal.fire({
                title: "¿Qué deseas hacer?",
                icon: "warning",
                showCancelButton: true,
                showDenyButton: true,
                confirmButtonText: "Eliminar con devolución",
                denyButtonText: "Eliminar completamente",
                cancelButtonText: "Cancelar",
                confirmButtonColor: "#28a745",
                denyButtonColor: "#d33",
                cancelButtonColor: "#6c757d"
            }).then((result) => {
                let url = '';
                if (result.isConfirmed) {
                    url = `/bodega/entradas/eliminar/${entradaId}/?devolver=1`;
                } else if (result.isDenied) {
                    url = `/bodega/entradas/eliminar/${entradaId}/?devolver=0`;
                }

                if (url !== '') {
                    fetch(url, {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": csrfToken
                        }
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                Swal.fire("Eliminado", "La entrada fue eliminada correctamente.", "success")
                                    .then(() => location.reload());
                            } else {
                                Swal.fire("Error", "No se pudo eliminar la entrada.", "error");
                            }
                        })
                        .catch(() => {
                            Swal.fire("Error", "Hubo un problema con la solicitud.", "error");
                        });
                }
            });
        });
    });
});

// Insumos
//Inventario local
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-insumo").forEach(button => {
        button.addEventListener("click", function () {
            let insumoId = this.getAttribute("data-id");

            Swal.fire({
                title: "¿Deseas eliminar este insumo?",
                text: "Una vez eliminado, no podrás recuperarlo.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                cancelButtonColor: "#3085d6",
                confirmButtonText: "Sí, eliminar",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`/bodega/insumos/eliminar/${insumoId}/`, {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": csrfToken
                        }
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                Swal.fire("Eliminado", "El insumo ha sido eliminado.", "success")
                                    .then(() => location.reload());
                            } else {
                                Swal.fire("Error", "No se pudo eliminar el insumo.", "error");
                            }
                        })
                        .catch(error => {
                            Swal.fire("Error", "Hubo un problema con la solicitud.", "error");
                        });
                }
            });
        });
    });
});