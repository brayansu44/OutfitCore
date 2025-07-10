
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