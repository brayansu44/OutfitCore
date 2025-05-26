let smartwizard = document.getElementById("smartwizard");
let dataId = smartwizard.getAttribute("data-id");

var steps = ["step-1", "step-2", "step-3", "step-4"];
var step = steps.indexOf(dataId);
if (step === -1) {
    step = 0;
}

//DETONANTE DE VIEWS SEGURIDAD SOCIAL CON EL FORM
document.addEventListener('DOMContentLoaded', function() {
    
    const form = document.getElementById(`FormEPS`);
    const submitAdd = document.getElementById(`submitAddEPS`); // OBTIENE LA URL DE LAS VIEWS "add" DE SEGURIDAD SOCIAL
    const messagesContainer = document.getElementById('messagesContainer');

    if (form && submitAdd) {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // ¡PREVENIR EL ENVÍO NORMAL DEL FORMULARIO!

            const addUrl = submitAdd.getAttribute('data-add-url');
            if (!addUrl) {
                console.error("URL no definida en el botón.");
                return;
            }

            // Obtener los datos del formulario
            const formData = new FormData(form);
            // Opcional: añadir el token CSRF si no está ya en FormData (FormData lo debería incluir)
            // const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            // formData.append('csrfmiddlewaretoken', csrftoken);

            fetch(addUrl, {
                method: 'POST',
                body: formData,
                // Si no usas FormData y envías JSON, necesitas Headers:
                // headers: {
                //     'Content-Type': 'application/json',
                //     'X-CSRFToken': csrftoken, // Incluir el token CSRF
                // },
                // body: JSON.stringify({
                //     nombre_eps: form.elements['nombre_eps'].value,
                //     nit_eps: form.elements['nit_eps'].value,
                // })
            })
            .then(response => {
                // Si la vista EPSadd devuelve JSON:
                if (response.headers.get('Content-Type').includes('application/json')) {
                    return response.json();
                }
                // Si devuelve HTML:
                return response.text(); 
            })
            .then(data => {
                // Asumiendo que la vista EPSadd devuelve JSON con 'success' y 'message'
                if (typeof data === 'object' && data.success) {
                    messagesContainer.innerHTML = `<p style="color: green;">${data.message}</p>`;
                    form.reset(); // Limpiar el formulario
                    // Aquí podrías actualizar una tabla de EPS dinámicamente si tienes una
                } else if (typeof data === 'object' && data.message) {
                    messagesContainer.innerHTML = `<p style="color: red;">${data.message}</p>`;
                } else {
                    // Si la vista devuelve HTML (ej. errores de formulario renderizados)
                    messagesContainer.innerHTML = `<p style="color: blue;">Respuesta del servidor:</p>${data}`;
                }
            })
            .catch(error => {
                console.error('Error al enviar el formulario:', error);
                messagesContainer.innerHTML = `<p style="color: red;">Ocurrió un error en la solicitud.</p>`;
            });
        });
    }
});

//EDITAR EPS
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
 

//DINAMICA DEL SMARTWIZARD
const eps ="EPS";
const arl = "ARL";
const pension = "PENSIÓN";
const caja = "CAJA DE COMPENSACIÓN";

$(document).ready(function () {
    var aux = ""; //VARIABLE AUXILIAR TEMPORAL DENTRO DE LA FUNCION "Div_dynamic"

    document.getElementById("btnMostrarEPS").addEventListener("click", function(event) {
        if (event.type === "click") {
            aux = eps;
            Div_dynamic();
        }
    });


    function Div_dynamic() {
        if (aux === eps){
            const btnMostrarEPS = document.getElementById("btnMostrarEPS");
            btnMostrarEPS.textContent = btnMostrarEPS.textContent === "Añadir" ? "Consultar" : "Añadir";
        }

        let Add = document.getElementById(`Add${aux}`);
        let View = document.getElementById(`View${aux}`);

        //REGISTRAR
        if (View.style.display === "block" && Add.style.display === "none"){

            document.getElementById(`Title${aux}`).textContent = `REGISTRAR ${aux}`;

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
        
        //CONSULTAR
        }else{
            
            document.getElementById(`Title${aux}`).textContent = `LISTA DE ${aux}`;

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