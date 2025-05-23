var selectedTabId = "{{ tab_id }}";
var steps = ["step-1", "step-2", "step-3", "step-4"];
var step = steps.indexOf(selectedTabId);
if (step === -1) step = 0;

//EPS
const btnMostrarEPS = document.getElementById("btnMostrarEPS");
const BtnAddEPS = document.getElementById("BtnAddEPS");
if (btnMostrarEPS || BtnAddEPS){
    btnMostrarEPS.addEventListener("click", EPS);
    BtnAddEPS.addEventListener("click", EPS);
}

function EPS() {
    btnMostrarEPS.textContent = btnMostrarEPS.textContent === "Añadir" ? "Consultar" : "Añadir";

    let AddEPS = document.getElementById("AddEPS");
    let ViewEPS = document.getElementById("ViewEPS");

    if (ViewEPS.style.display === "block" && AddEPS.style.display === "none"){
        document.getElementById("TitleEPS").textContent = "REGISTRAR EPS";
        AddEPS.style.opacity = "0";
        AddEPS.style.display = "block";

        ViewEPS.style.opacity = "1";
        ViewEPS.style.display = "none";
        
        setTimeout(() => {
            AddEPS.style.opacity = "1";
            AddEPS.style.transition = "opacity 0.5s ease-in-out";

            ViewEPS.style.opacity = "0";
            ViewEPS.style.transition = "opacity 0.5s ease-in-out";
        }, 100);

        $('#smartwizard').smartWizard("reset");
        return true;

    }else{
        document.getElementById("TitleEPS").textContent = "LISTA DE EPS";
        ViewEPS.style.opacity = "0";
        ViewEPS.style.display = "block";

        AddEPS.style.opacity = "1";
        AddEPS.style.display = "none";

        setTimeout(() => {
            ViewEPS.style.opacity = "1";
            ViewEPS.style.transition = "opacity 0.5s ease-in-out";

            AddEPS.style.opacity = "0";
            AddEPS.style.transition = "opacity 0.5s ease-in-out";
        }, 100);

        $('#smartwizard').smartWizard("reset");
        return true;
    }
    
};

$(document).ready(function () {
    // Step show event
    $("#smartwizard").on("showStep", function (e, anchorObject, stepNumber, stepDirection, stepPosition) {
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