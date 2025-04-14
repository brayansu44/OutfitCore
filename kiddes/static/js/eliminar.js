
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
