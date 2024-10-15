

$(document).ready(function () {
  $('#form-data-table').DataTable();
});



// Use jQuery to listen for the modal 'hidden' event
$('#robo_detailsModal').on('hidden.bs.modal', function () {
  $('#RoboForm')[0].reset();
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
    document.getElementById('location').value = client_location;
  } else {
    document.getElementById('location').value = null;
  }
  
});



document.getElementById('robot_id').addEventListener('change', function () {
  var selectedOption = this.options[this.selectedIndex];
  var robo_name = selectedOption.getAttribute('data-robo-name');
  var robo_type = selectedOption.getAttribute('data-robo-type');

  if (robo_name) {
    document.getElementById('robot_name').value = robo_name;
  } else {
    document.getElementById('robot_name').value = null;
  }

  if (robo_type) {
    document.getElementById('robot_type').value = robo_type;
  } else {
    document.getElementById('robot_type').value = null;
  }
  
});
