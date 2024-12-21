
// Jquery datatables script
$(document).ready(function () {
  $('#form_data_table').DataTable();
});



// Use jQuery to listen for the modal 'hidden' event
$('#materialcostModal').on('hidden.bs.modal', function () {
  // Reset the form fields
  $('#materialcostForm')[0].reset();
});



document.getElementById('client_id').addEventListener('change', function () {
  var selectedOption = this.options[this.selectedIndex];
  var clientName = selectedOption.getAttribute('data-client-name');
  var client_location = selectedOption.getAttribute('data-location');

  if (clientName) {
    document.getElementById('client_name').value = clientName;
  } else {
    document.getElementById('client_name').value = null;
  }

  if (client_location) {
    document.getElementById('client_location').value = client_location;
  } else {
    document.getElementById('client_location').value = null;
  }
  
});


document.getElementById('material_name').addEventListener('change', function () {
  var selectedOption = this.options[this.selectedIndex];
  var material_code = selectedOption.getAttribute('data-material-code');
  var hsn_code = selectedOption.getAttribute('data-hsn-code');

  if (material_code) {
    document.getElementById('material_code').value = material_code;
  } else {
    document.getElementById('material_code').value = null;
  }
  if (hsn_code) {
    document.getElementById('hsn_code').value = hsn_code;
  } else {
    document.getElementById('hsn_code').value = null;
  }

});






