

function enable_form1(action) {
    var inputs = document.querySelectorAll('#form1 .editable-input');
    inputs.forEach(function (input) {
        input.classList.add('active'); 
        input.removeAttribute('readonly');
    });

    var toggleBtn = document.getElementById('toggle_btn_1');
    if (action === 'edit' || action === 'add') {
        toggleBtn.style.display = 'none';
    }
    document.getElementById('submit_1').style.display = 'block';
}



function enable_form2(action) {
    var inputs = document.querySelectorAll('#form2 .editable-input');
    inputs.forEach(function (input) {
        input.classList.add('active'); 
        input.removeAttribute('readonly');
    });

    var toggleBtn = document.getElementById('toggle_btn_2');
    if (action === 'edit' || action === 'add') {
        toggleBtn.style.display = 'none';
    }
    document.getElementById('submit_2').style.display = 'block';
}

function enable_form3(action) {
    var inputs = document.querySelectorAll('#form3 .editable-input');
    inputs.forEach(function (input) {
        input.classList.add('active'); 
        input.removeAttribute('readonly');
    });

    var toggleBtn = document.getElementById('toggle_btn_3');
    if (action === 'edit' || action === 'add') {
        toggleBtn.style.display = 'none';
    }
    document.getElementById('submit_3').style.display = 'block';
}

function enable_form4(action) {
    var inputs = document.querySelectorAll('#form4 .editable-input');
    inputs.forEach(function (input) {
        input.classList.add('active'); 
        input.removeAttribute('readonly');
    });

    var toggleBtn = document.getElementById('toggle_btn_4');
    if (action === 'edit' || action === 'add') {
        toggleBtn.style.display = 'none';
    }
    document.getElementById('submit_4').style.display = 'block';
}
