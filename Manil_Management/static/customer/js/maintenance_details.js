
$(document).ready(function () {
  $('#form-data-table').DataTable();
});



// Use jQuery to listen for the modal 'hidden' event
$('#maintenanceModal').on('hidden.bs.modal', function () {
  $('#MaintenanceForm')[0].reset();
});
