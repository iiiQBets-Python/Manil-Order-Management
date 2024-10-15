
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


document.getElementById('material_code').addEventListener('change', function () {
  var selectedOption = this.options[this.selectedIndex];
  var material_name = selectedOption.getAttribute('data-material-name');

  if (material_name) {
    document.getElementById('material_name').value = material_name;
  } else {
    document.getElementById('material_name').value = null;
  }
});


