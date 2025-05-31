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
function Div_dynamic(aux_temporal) {
    let stepNow = $("#smartwizard").smartWizard("getStepIndex"); // Obtiene el paso actual

    if (aux_temporal === eps){
        const btnMostrarEPS = document.getElementById("btnMostrarEPS");
        btnMostrarEPS.textContent = btnMostrarEPS.textContent === "Añadir" ? "Consultar" : "Añadir";
    }

    let Add = document.getElementById(`Add${aux_temporal}`);
    let View = document.getElementById(`View${aux_temporal}`);

    //REGISTRAR
    if (View.style.display === "block" && Add.style.display === "none"){

        document.getElementById(`Title${aux_temporal}`).textContent = `REGISTRAR ${aux_temporal}`;

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

//DETONANTE DE VIEWS SEGURIDAD SOCIAL CON EL FORM
function detonadorViews(form, submit) {
    
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

//Cambio de Paso en el SmartWizard dinamico
function changeTabID(aux_temporal) {
    let nuevaURL = new URL(window.location.href);
    nuevaURL.pathname = `/nomina/SeguridadSocial/${aux_temporal}/`;
    window.history.pushState(null, "", nuevaURL.toString());
}
 
//FUNCIONES CRUD
$(document).ready(function () {

    document.getElementById("btnMostrarEPS").addEventListener("click", function(event) {
        if (event.type === "click") {
            aux = window.location.hash; // Captura el ID del paso smartwizard
            aux = aux.replace("#", ""); // Elimina el símbolo "#"
            changeTabID(aux)

            //REGISTRAR FORM
            const form = document.getElementById(`Form${aux}`);
            const submit = document.getElementById(`submitAdd${aux}`);
            Div_dynamic(aux);
            detonadorViews(form, submit)
        }
    });

    document.getElementById("BtnEditEPS").addEventListener("click", function(event) {
        if (event.type === "click") {
            aux = window.location.hash; // Captura el ID del paso smartwizard
            aux = aux.replace("#", ""); // Elimina el símbolo "#"
            changeTabID(aux)

            //EDITAR FORM
            const form = document.getElementById(`Form${aux}`);
            const submit = document.getElementById(`submitEdit${aux}`);
            Div_dynamic(aux);
            detonadorViews(form, submit)
        }
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