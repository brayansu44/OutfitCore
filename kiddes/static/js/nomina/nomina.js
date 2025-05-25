let smartwizard = document.getElementById("smartwizard");
let dataId = smartwizard.getAttribute("data-id");

var steps = ["step-1", "step-2", "step-3", "step-4"];
var step = steps.indexOf(dataId);
if (step === -1) {
    step = 0;
}


document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".btn-info").forEach(button => {
        button.addEventListener("click", function () {
            let ID = this.closest("tr").querySelector(".delete-eps").getAttribute("data-id");

            fetch(`/nomina/SeguridadSocial/step-1/${ID}/`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById("nombre").value = data.nombre;
                    document.getElementById("direccion").value = data.direccion;
                    document.getElementById("telefono").value = data.telefono;
                    document.getElementById("correo").value = data.correo;
                    document.getElementById("estado").value = data.estado;
                })
                .catch(error => console.error("Error en la solicitud:", error));
        });
    });
});


const eps ="EPS";
const arl = "ARL";
const pension = "PENSION";
const caja = "CAJA";

const btnMostrarEPS = document.getElementById("btnMostrarEPS");
const BtnAddEPS = document.getElementById("BtnAddEPS");
const BtnEditEPS = document.getElementById("BtnEditEPS");


$(document).ready(function () {
    var aux = "";
    if (btnMostrarEPS || BtnAddEPS || BtnEditEPS){
        aux = eps;
        btnMostrarEPS.addEventListener("click", Div_dynamic);
        BtnAddEPS.addEventListener("click", Div_dynamic);
        BtnEditEPS.addEventListener("click", Div_dynamic);
    }

    function Div_dynamic() {
        if (aux === "EPS"){
            btnMostrarEPS.textContent = btnMostrarEPS.textContent === "Añadir" ? "Consultar" : "Añadir";
        }


        let Add = document.getElementById(`Add${aux}`);
        let View = document.getElementById(`View${aux}`);

        if (View.style.display === "block" && Add.style.display === "none"){

            if(aux === "EPS"){
                document.getElementById("TitleEPS").textContent = "REGISTRAR EPS";
            }

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

            $('#smartwizard').smartWizard("reset");
            return true;

        }else{
            if(aux === "EPS"){
                document.getElementById("TitleEPS").textContent = "LISTA DE EPS";
            }

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

            $('#smartwizard').smartWizard("reset");
            return true;
        }
    };
    
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
            animation: 'fade', // none/fade/slide-horizontal/slide-vertical/slide-swing
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