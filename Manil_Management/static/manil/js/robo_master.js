

$(document).ready(function () {
    $('#form-data-table').DataTable();
  });
  
  
  
  // Use jQuery to listen for the modal 'hidden' event
  $('#roboModal').on('hidden.bs.modal', function () {
    $('#RoboForm')[0].reset();
  });
  