// Jquery datatables script


$(document).ready(function () {
  $('#form_data_table').DataTable();
});



// Use jQuery to listen for the modal 'hidden' event
$('#clientModal').on('hidden.bs.modal', function () {
  $('#ClientForm')[0].reset();
});


var billing_address = document.getElementById('billing_address');
var billing_city = document.getElementById('billing_city');
var billing_state = document.getElementById('billing_state');
var billing_pin = document.getElementById('billing_pin');
var billing_gst_number = document.getElementById('billing_gst_number');



var sameAsBilling = document.getElementById('sameAsBilling');
var billingTab = document.getElementById('billing-tab');
var shippingTab = document.getElementById('shipping-tab');

var next_btn = document.getElementById('next_btn');
var submit_btn = document.getElementById('submit_btn');

var shippingFields = {
  address: document.getElementById('shipping_address'),
  city: document.getElementById('shipping_city'),
  state: document.getElementById('shipping_state'),
  pin: document.getElementById('shipping_pin'),
  gst_number: document.getElementById('shipping_gst_number'),
};

var billingFields = {
  address: document.getElementById('billing_address'),
  city: document.getElementById('billing_city'),
  state: document.getElementById('billing_state'),
  pin: document.getElementById('billing_pin'),
  gst_number: document.getElementById('billing_gst_number'),
};



function next_btn_enable(){  
  if (billing_address.value && billing_city.value && billing_state.value && billing_pin.value && billing_gst_number.value){
    next_btn.disabled = false;
  } else{
    next_btn.disabled = true;
  }
}


function move_next() {

  if (next_btn.disabled == false){
    shippingTab.click();
    next_btn.style.display = 'none';
    submit_btn.style.display = 'block';
  } else {
    if (!billing_gst_number.value) {
      billing_gst_number.setCustomValidity("Please Fill this field");
      billing_gst_number.reportValidity();      
    }
    if (!billing_pin.value) {
      billing_pin.setCustomValidity("Please Fill this field");
      billing_pin.reportValidity();      
    }
    if (!billing_state.value) {
      billing_state.setCustomValidity("Please Fill this field");
      billing_state.reportValidity();      
    }
    if (!billing_city.value) {
      billing_city.setCustomValidity("Please Fill this field");
      billing_city.reportValidity();      
    }
    if (!billing_address.value) {
      billing_address.setCustomValidity("Please Fill this field");
      billing_address.reportValidity();      
    } 
  }
}



function check_validate() {
  if (sameAsBilling.checked == true) {
          
    for (let key in shippingFields) {
      shippingFields[key].value = null;
      shippingFields[key].removeAttribute('required');
      shippingFields[key].disabled = true;
    }

    shippingTab.style.display = 'none';
    next_btn.style.display = 'none';
    submit_btn.style.display = 'block';
    billingTab.click();
  } else {

    for (let key in shippingFields) {
      shippingFields[key].value = null;
      shippingFields[key].setAttribute('required', 'required'); 
      shippingFields[key].disabled = false;
    }

    for (let key in billingFields) {      
      billingFields[key].removeAttribute('required');     
    }

    shippingTab.style.display = 'block';
    next_btn.style.display = 'block'; 
    submit_btn.style.display = 'none';
  }
}


document.getElementById('client_S_name').addEventListener('input', function () {
  let inputVal = this.value;

  if (inputVal.length >= 2) { // Start searching after 2 characters are typed
    fetch(`get_sname_matches?query=${inputVal}`)
      .then(response => response.json())
      .then(data => {
        let datalist = document.getElementById('snameList');
        datalist.innerHTML = ''; // Clear previous options

        // Populate datalist with matching results
        data.matches.forEach(function (sname) {
          let option = document.createElement('option');
          option.value = sname;
          datalist.appendChild(option);
        });
      })
      .catch(error => console.error('Error fetching suggestions:', error));
  }
});

document.addEventListener('DOMContentLoaded', function () {
  next_btn_enable();
});

