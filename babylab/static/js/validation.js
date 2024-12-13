// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict';
    window.addEventListener('load', function () {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();

function validateForm() {
    let l1 = document.forms["questionnaire-input"]["inputLang1"].value;
    let l2 = document.forms["questionnaire-input"]["inputLang2"].value;
    let l3 = document.forms["questionnaire-input"]["inputLang3"].value;
    let l4 = document.forms["questionnaire-input"]["inputLang4"].value;
    let e1 = parseFloat(document.forms["questionnaire-input"]["inputLang1Exp"].value);
    let e2 = parseFloat(document.forms["questionnaire-input"]["inputLang2Exp"].value);
    let e3 = parseFloat(document.forms["questionnaire-input"]["inputLang3Exp"].value);
    let e4 = parseFloat(document.forms["questionnaire-input"]["inputLang4Exp"].value);
    let array = [l1, l2, l3, l4]
    let duplicates = array.filter((item, index) => array.indexOf(item) !== index);
    let duplicates_filtered = duplicates.filter(i => i !== "0");

    if (duplicates_filtered.length !== 0) {
        customAlert.alert('At least one language is repeated', 'Input error');
        return false;
    }
    if ((e1 + e2 + e3 + e4) != 100) {
        customAlert.alert('Percentages must add up to 100 %.', 'Input error');
        return false;
    }

    if (l1 == "0" & e1 != 0) {
        customAlert.alert('Language 1 is not selected but exposure is not 0%.', 'Input error')
        return false;
    }
    if (l2 == "0" & e2 != 0) {
        customAlert.alert('Language 2 is not selected but exposure is not 0%.', 'Input error')
        return false;
    }
    if (l3 == "0" & e3 != 0) {
        customAlert.alert('Language 3 is not selected but exposure is not 0%.', 'Input error')
        return false;
    }
    if (l4 == "0" & e4 != 0) {
        customAlert.alert('Language 4 is not selected but exposure is not 0%.', 'Input error')
    }
    if (l1 != "0" & e1 == 0) {
        customAlert.alert('Language 1 is selected but exposure is 0%.', 'Input error')
        return false;
    }
    if (l2 != "0" & e2 == 0) {
        customAlert.alert('Language 2 is selected but exposure is 0%.', 'Input error')
        return false;
    }
    if (l3 != "0" & e3 == 0) {
        customAlert.alert('Language 3 is selected but exposure is 0%.', 'Input error')
        return false;
    }
    if (l4 != "0" & e4 == 0) {
        customAlert.alert('Language 4 is selected but exposure is 0%.', 'Input error')
        return false;
    }


}