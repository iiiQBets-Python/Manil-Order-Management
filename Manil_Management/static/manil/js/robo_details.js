

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

document.querySelectorAll('[id^="client_id-"]').forEach(function (clientIdElement) {
  clientIdElement.addEventListener('change', function () {
    var selectedOption = this.options[this.selectedIndex];
    var modalId = this.id.split('-')[1]; // Extract the modal ID
    var clientName = selectedOption.getAttribute('data-client-name');
    var clientLocation = selectedOption.getAttribute('data-location');

    var clientNameField = document.getElementById(`client_name-${modalId}`);
    var clientLocationField = document.getElementById(`location-${modalId}`);

    if (clientName) {
      clientNameField.value = clientName;
    } else {
      clientNameField.value = null;
    }

    if (clientLocation) {
      clientLocationField.value = clientLocation;
    } else {
      clientLocationField.value = null;
    }
  });
});

document.querySelectorAll('[id^="robot_id-"]').forEach(function (robotIdElement) {
  robotIdElement.addEventListener('change', function () {
    var selectedOption = this.options[this.selectedIndex];
    var modalId = this.id.split('-')[1]; // Extract the modal ID
    var roboName = selectedOption.getAttribute('data-robo-name');
    var roboType = selectedOption.getAttribute('data-robo-type');

    var robotNameField = document.getElementById(`robot_name-${modalId}`);
    var robotTypeField = document.getElementById(`robot_type-${modalId}`);

    if (roboName) {
      robotNameField.value = roboName;
    } else {
      robotNameField.value = null;
    }

    if (roboType) {
      robotTypeField.value = roboType;
    } else {
      robotTypeField.value = null;
    }
  });
});