let smartwizard = document.getElementById("smartwizard");
let dataId = smartwizard.getAttribute("data-id");

//DINAMICA DEL SMARTWIZARD
const eps ="EPS";
const arl = "ARL";
const pension = "PENSION";
const caja = "CAJA";

var steps = [eps, arl, pension, caja];
var step = steps.indexOf(dataId);
if (step === -1) {
    step = 0;
}

//Visualizacion dinamica de div dentro del Smartwizard
function Div_dynamic(aux_temporal, accion) {
    let stepNow = $("#smartwizard").smartWizard("getStepIndex"); // Obtiene el paso actual
    let Add = document.getElementById(`Add${aux_temporal}`);
    let View = document.getElementById(`View${aux_temporal}`);
    let submitAdd = document.getElementById(`submitAdd${aux_temporal}`);
    let submitEdit = document.getElementById(`submitEdit${aux_temporal}`);

    const btnMostrar = document.getElementById(`btnMostrar${aux_temporal}`)
    btnMostrar.textContent = btnMostrar.textContent === "Añadir" ? "Consultar" : "Añadir";
    
    btnMostrar.addEventListener("click", function(event) {
        if (event.type === "click") {
            btnMostrar.textContent = btnMostrar.textContent === "Añadir" ? "Consultar" : "Añadir";
            submitAdd.style.opacity = "0";
            submitAdd.style.display = "block";

            submitEdit.style.opacity = "1";
            submitEdit.style.display = "none";
            
            setTimeout(() => {
                submitAdd.style.opacity = "1";
                submitAdd.style.transition = "opacity 0.5s ease-in-out";

                submitEdit.style.opacity = "0";
                submitEdit.style.transition = "opacity 0.5s ease-in-out";
            }, 100);
        }
    });

    document.querySelectorAll(".editar-eps").forEach(button => {
        button.addEventListener("click", function () {
            submitEdit.style.opacity = "0";
            submitEdit.style.display = "block";

            submitAdd.style.opacity = "1";
            submitAdd.style.display = "none";
            
            setTimeout(() => {
                submitEdit.style.opacity = "1";
                submitEdit.style.transition = "opacity 0.5s ease-in-out";

                submitAdd.style.opacity = "0";
                submitAdd.style.transition = "opacity 0.5s ease-in-out";
            }, 100);

        });
    });

    btnMostrar.addEventListener("click", function(event) {
        if (event.type === "click") {
            btnMostrar.textContent = btnMostrar.textContent === "Añadir" ? "Consultar" : "Añadir";
            submitAdd.style.opacity = "0";
            submitAdd.style.display = "block";

            submitEdit.style.opacity = "1";
            submitEdit.style.display = "none";
            
            setTimeout(() => {
                submitAdd.style.opacity = "1";
                submitAdd.style.transition = "opacity 0.5s ease-in-out";

                submitEdit.style.opacity = "0";
                submitEdit.style.transition = "opacity 0.5s ease-in-out";
            }, 100);
        }
    });

    //REGISTRAR
    if (View.style.display === "block" && Add.style.display === "none"){

        document.getElementById(`Title${aux_temporal}`).textContent = `${accion} ${aux_temporal}`;

        Add.style.opacity = "0";
        Add.style.display = "block";

        View.style.opacity = "1";
        View.style.display = "none";
        
        setTimeout(() => {
            Add.style.opacity = "1";
            Add.style.transition = "opacity 0.5s ease-in-out";

            View.style.opacity = "0";
            View.style.transition = "opacity 0.5s ease-in-out";
        }, 100);

        changeTabID(aux_temporal);

        
        $("#smartwizard").smartWizard("reset"); // Resetea el wizard
        $("#smartwizard").smartWizard("goToStep", stepNow); // Vuelve al paso guardado
        return true;
    
    //CONSULTAR
    }else{
        
        document.getElementById(`Title${aux_temporal}`).textContent = `LISTA DE ${aux_temporal}`;

        View.style.opacity = "0";
        View.style.display = "block";

        Add.style.opacity = "1";
        Add.style.display = "none";

        setTimeout(() => {
            View.style.opacity = "1";
            View.style.transition = "opacity 0.5s ease-in-out";

            Add.style.opacity = "0";
            Add.style.transition = "opacity 0.5s ease-in-out";
        }, 100);

        changeTabID(aux_temporal);

        $('#smartwizard').smartWizard("reset");
        $("#smartwizard").smartWizard("goToStep", stepNow); // Vuelve al paso guardado
        return true;
    }
};

//DETONANTE DE VIEWS "add" SEGURIDAD SOCIAL CON EL FORM
function ViewAdd(form, submit) {
    
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // ¡PREVENIR EL ENVÍO NORMAL DEL FORMULARIO!

        const addUrl = submit.getAttribute('data-add-url');
        if (!addUrl) {
            console.error("URL no definida en el botón.");
            return;
        }
        // Obtener los datos del formulario
        const formData = new FormData(form);
        fetch(addUrl, {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Error en la solicitud al servidor.");
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                Swal.fire("Agregado", data.message, "success")
                    .then(() => location.reload());
            } else {
                Swal.fire("Error", data.message, "error");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            Swal.fire("Error", "Hubo un problema con la solicitud.", "error");
        });
    });
}

//DETONANTE DE VIEWS "edit"
function ViewField(aux, id) {

    fetch(`/nomina/SeguridadSocial/${aux}/edit/${id}/`)
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Datos recibidos:", data.data); // Para depurar en la consola

            // Asigna los valores correctamente al formulario
            Object.keys(data.data).forEach(field => {
                let input = document.querySelector(`[name="${field}"]`);
                if (input) {
                    input.value = data.data[field];
                } else {
                    console.warn(`Campo '${field}' no encontrado en el formulario.`);
                }
            });
        } else {
            console.error("Error al obtener los datos.");
        }
    })
    .catch(error => console.error("Error en la solicitud AJAX:", error));
}

//DETONANTE DE VIEWS "edit" SEGURIDAD SOCIAL CON EL FORM
function ViewEdit(form, aux, id) {
    
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // ¡PREVENIR EL ENVÍO NORMAL DEL FORMULARIO!

        const addUrl = `/nomina/SeguridadSocial/${aux}/edit/${id}/`;
        if (!addUrl) {
            console.error("URL no definida en el botón.");
            return;
        }
        // Obtener los datos del formulario
        const formData = new FormData(form);
        fetch(addUrl, {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Error en la solicitud al servidor.");
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                Swal.fire("Agregado", data.message, "success")
                    .then(() => location.reload());
            } else {
                Swal.fire("Error", data.message, "error");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            Swal.fire("Error", "Hubo un problema con la solicitud.", "error");
        });
    });
}

function ViewDelete(aux, id) {
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
            fetch(`/nomina/SeguridadSocial/${aux}/delete/${id}/`, {
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
                        Swal.fire("Error", `No se pudo eliminar la ${aux}.`, "error");
                    }
                })
                .catch(error => {
                    Swal.fire("Error", "Hubo un problema con la solicitud.", "error");
                });
        }
    });
}

//Cambio de Paso en el SmartWizard dinamico
function changeTabID(aux_temporal) {
    let nuevaURL = new URL(window.location.href);
    nuevaURL.pathname = `/nomina/SeguridadSocial/${aux_temporal}/`;
    window.history.pushState(null, "", nuevaURL.toString());
}
 
//FUNCIONES CRUD
document.addEventListener("DOMContentLoaded", function () {

    ///EPS
    document.getElementById("btnMostrarEPS").addEventListener("click", function(event) {
        if (event.type === "click") {
            aux = window.location.hash; // Captura el ID del paso smartwizard
            aux = aux.replace("#", ""); // Elimina el símbolo "#"
            changeTabID(aux)

            //REGISTRAR FORM
            const form = document.getElementById(`Form${aux}`);
            const submit = document.getElementById(`submitAdd${aux}`);
            Div_dynamic(aux, "REGISTRAR ");
            ViewAdd(form, submit)
        }
    });

    document.querySelectorAll(".editar-eps").forEach(button => {
        button.addEventListener("click", function () {
            aux = window.location.hash; // Captura el ID del paso smartwizard
            aux = aux.replace("#", ""); // Elimina el símbolo "#"
            changeTabID(aux)

            //EDITAR
            let id = this.getAttribute("data-id");
            const form = document.getElementById(`Form${aux}`);
            
            Div_dynamic(aux, "EDITAR ");
            ViewField(aux, id);
            ViewEdit(form, aux, id)

        });
    });

    document.querySelectorAll(".delete-eps").forEach(button => {
        button.addEventListener("click", function () {
            aux = window.location.hash; // Captura el ID del paso smartwizard
            aux = aux.replace("#", ""); // Elimina el símbolo "#"
            changeTabID(aux)

            let id = this.getAttribute("data-id");
            
            ViewDelete(aux, id)

        });
    });

    ///ARL
    document.getElementById("btnMostrarARL").addEventListener("click", function(event) {
        if (event.type === "click") {
            aux = window.location.hash; // Captura el ID del paso smartwizard
            aux = aux.replace("#", ""); // Elimina el símbolo "#"
            changeTabID(aux)

            //REGISTRAR FORM
            const form = document.getElementById(`Form${aux}`);
            const submit = document.getElementById(`submitAdd${aux}`);
            Div_dynamic(aux, "REGISTRAR ");
            ViewAdd(form, submit)
        }
    });

    document.querySelectorAll(".editar-arl").forEach(button => {
        button.addEventListener("click", function () {
            aux = window.location.hash; // Captura el ID del paso smartwizard
            aux = aux.replace("#", ""); // Elimina el símbolo "#"
            changeTabID(aux)

            //EDITAR
            let id = this.getAttribute("data-id");
            const form = document.getElementById(`Form${aux}`);
            
            Div_dynamic(aux, "EDITAR ");
            ViewField(aux, id);
            ViewEdit(form, aux, id)

        });
    });

    document.querySelectorAll(".delete-arl").forEach(button => {
        button.addEventListener("click", function () {
            aux = window.location.hash; // Captura el ID del paso smartwizard
            aux = aux.replace("#", ""); // Elimina el símbolo "#"
            changeTabID(aux)

            let id = this.getAttribute("data-id");
            
            ViewDelete(aux, id)

        });
    });

    ///PENSION
    document.getElementById("btnMostrarPENSION").addEventListener("click", function(event) {
        if (event.type === "click") {
            aux = window.location.hash; // Captura el ID del paso smartwizard
            aux = aux.replace("#", ""); // Elimina el símbolo "#"
            changeTabID(aux)

            //REGISTRAR FORM
            const form = document.getElementById(`Form${aux}`);
            const submit = document.getElementById(`submitAdd${aux}`);
            Div_dynamic(aux, "REGISTRAR ");
            ViewAdd(form, submit)
        }
    });

    document.querySelectorAll(".editar-pension").forEach(button => {
        button.addEventListener("click", function () {
            aux = window.location.hash; // Captura el ID del paso smartwizard
            aux = aux.replace("#", ""); // Elimina el símbolo "#"
            changeTabID(aux)

            //EDITAR
            let id = this.getAttribute("data-id");
            const form = document.getElementById(`Form${aux}`);
            
            Div_dynamic(aux, "EDITAR ");
            ViewField(aux, id);
            ViewEdit(form, aux, id)

        });
    });

    document.querySelectorAll(".delete-pension").forEach(button => {
        button.addEventListener("click", function () {
            aux = window.location.hash; // Captura el ID del paso smartwizard
            aux = aux.replace("#", ""); // Elimina el símbolo "#"
            changeTabID(aux)

            let id = this.getAttribute("data-id");
            
            ViewDelete(aux, id)

        });
    });

    ///CAJA
    document.getElementById("btnMostrarCAJA").addEventListener("click", function(event) {
        if (event.type === "click") {
            aux = window.location.hash; // Captura el ID del paso smartwizard
            aux = aux.replace("#", ""); // Elimina el símbolo "#"
            changeTabID(aux)

            //REGISTRAR FORM
            const form = document.getElementById(`Form${aux}`);
            const submit = document.getElementById(`submitAdd${aux}`);
            Div_dynamic(aux, "REGISTRAR ");
            ViewAdd(form, submit)
        }
    });

    document.querySelectorAll(".editar-caja").forEach(button => {
        button.addEventListener("click", function () {
            aux = window.location.hash; // Captura el ID del paso smartwizard
            aux = aux.replace("#", ""); // Elimina el símbolo "#"
            changeTabID(aux)

            //EDITAR
            let id = this.getAttribute("data-id");
            const form = document.getElementById(`Form${aux}`);
            
            Div_dynamic(aux, "EDITAR ");
            ViewField(aux, id);
            ViewEdit(form, aux, id)

        });
    });

    document.querySelectorAll(".delete-caja").forEach(button => {
        button.addEventListener("click", function () {
            aux = window.location.hash; // Captura el ID del paso smartwizard
            aux = aux.replace("#", ""); // Elimina el símbolo "#"
            changeTabID(aux)

            let id = this.getAttribute("data-id");
            
            ViewDelete(aux, id)

        });
    });

});


//smartwizard
$(document).ready(function () {
    // Step show event
    $("#smartwizard").on("showStep", function (stepPosition) {
        $("#prev-btn").removeClass('disabled');
        $("#next-btn").removeClass('disabled');
        if (stepPosition === 'first') {
            $("#prev-btn").addClass('disabled');
        } else if (stepPosition === 'last') {
            $("#next-btn").addClass('disabled');
        } else {
            $("#prev-btn").removeClass('disabled');
            $("#next-btn").removeClass('disabled');
        }
        
    });
    // Smart Wizard
    $('#smartwizard').smartWizard({
        selected: step,
        theme: 'dots',
        transition: {
            animation: 'none', // none/fade/slide-horizontal/slide-vertical/slide-swing
        },
        toolbarSettings: {
            toolbarPosition: 'both',
        },
        anchorSettings: {
            enableAllAnchors: true // pasos sin restricciones
        }
    });
    
    $("#prev-btn").on("click", function () {
        // Navigate previous
        $('#smartwizard').smartWizard("prev");
        return true;
        
    });
    $("#next-btn").on("click", function () {
        // Navigate next
        $('#smartwizard').smartWizard("next");
        return true;
    });

    

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