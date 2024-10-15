

function enable_form1() {
    var inputs = document.querySelectorAll('#form1 .editable-input');    
    inputs.forEach(function (input) {
        input.removeAttribute('readonly');
    });    
    document.getElementById('edit_1').style.display = 'none';
    document.getElementById('submit_1').style.display = 'block';
}


function enable_form2() {
    var inputs = document.querySelectorAll('#form2 .editable-input');    
    inputs.forEach(function (input) {
        input.removeAttribute('readonly');
    });    
    document.getElementById('edit_2').style.display = 'none';
    document.getElementById('submit_2').style.display = 'block';
}


function enable_form3() {
    var inputs = document.querySelectorAll('#form3 .editable-input');    
    inputs.forEach(function (input) {
        input.removeAttribute('readonly');
    });    
    document.getElementById('edit_3').style.display = 'none';
    document.getElementById('submit_3').style.display = 'block';
}


function enable_form4() {
    var inputs = document.querySelectorAll('#form4 .editable-input');    
    inputs.forEach(function (input) {
        input.removeAttribute('readonly');
    });    
    document.getElementById('edit_4').style.display = 'none';
    document.getElementById('submit_4').style.display = 'block';
}