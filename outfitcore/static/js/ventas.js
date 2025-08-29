const prefix = 'detalles';
const container = document.getElementById('formset-container');
const addFormBtn = document.getElementById('add-form-btn');
const totalForms = document.querySelector(`#id_${prefix}-TOTAL_FORMS`);

function updateFormCount() {
    const forms = document.querySelectorAll('.formset-form');
    if (totalForms) totalForms.value = forms.length;
}

function cloneEmptyForm() {
    const forms = document.querySelectorAll('.formset-form');
    const newIndex = forms.length;
    const formRegex = new RegExp(`${prefix}-(\\d+)-`, 'g');

    const newForm = forms[0].cloneNode(true);
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `${prefix}-${newIndex}-`);

    newForm.querySelectorAll('input, select, textarea').forEach(el => {
        if (el.name && el.name.endsWith('-DELETE')) return;

        if (el.tagName.toLowerCase() === 'select') {
            el.selectedIndex = 0;
        } else if (el.type === 'checkbox' || el.type === 'radio') {
            el.checked = false;
        } else {
            el.value = '';
        }

        if (el.id) {
            el.id = el.id.replace(formRegex, `${prefix}-${newIndex}-`);
        }
    });

    newForm.querySelectorAll('label').forEach(lbl => {
        if (lbl.htmlFor) {
            lbl.htmlFor = lbl.htmlFor.replace(formRegex, `${prefix}-${newIndex}-`);
        }
    });

    container.appendChild(newForm);
    updateFormCount();
}

addFormBtn.addEventListener('click', cloneEmptyForm);

container.addEventListener('click', function (e) {
    if (e.target.closest('.remove-form-btn')) {
        const btn = e.target.closest('.remove-form-btn');
        const formDiv = btn.closest('.formset-form');
        const deleteCheckbox = formDiv.querySelector(`input[name$="-DELETE"]`);
        if (deleteCheckbox) {
            deleteCheckbox.checked = true;
            formDiv.style.display = 'none';
        } else {
            formDiv.remove();
        }
        updateFormCount();
    }
});


// ------------------ AJAX variantes por local ------------------
document.addEventListener("DOMContentLoaded", function () {
    const localSelect = document.getElementById("id_local");
    const urlVariantes = document.getElementById("url-obtener-variantes").value;
    const placeholder = document.getElementById("placeholder-variante").value;

    if (localSelect) {
        localSelect.addEventListener("change", function () {
            const localId = this.value;
            if (!localId) {
                document.querySelectorAll("select.detalle-variante").forEach(select => {
                    select.innerHTML = `<option value="">${placeholder}</option>`;
                });
                return;
            }

            fetch(`${urlVariantes}?local_id=${localId}`)
                .then(response => response.json())
                .then(data => {
                    document.querySelectorAll("select.detalle-variante").forEach(select => {
                        select.innerHTML = `<option value="">${placeholder}</option>`;
                        data.variantes.forEach(v => {
                            const opt = document.createElement("option");
                            opt.value = v.id;
                            opt.textContent = `${v.nombre} (Stock: ${v.stock})`;
                            select.appendChild(opt);
                        });
                    });
                })
                .catch(error => console.error("Error cargando variantes:", error));
        });
    }
});


// ------------------ Mostrar/Ocultar detalle según local ------------------
document.addEventListener("DOMContentLoaded", function () {
    const localSelect = document.getElementById("id_local");
    const detalleVentaSection = document.getElementById("detalle-venta-section");

    if (localSelect) {
        localSelect.addEventListener("change", function () {
            if (this.value) {
                detalleVentaSection.style.display = "block";
            } else {
                detalleVentaSection.style.display = "none";
            }
        });
    }
});


// Bootstrap validation
(function () {
    'use strict'

    var forms = document.querySelectorAll('.needs-validation');

    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }

            form.classList.add('was-validated');
        }, false);
    });
})()
