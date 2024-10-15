
$(document).ready(function () {
    $('#form-data-table').DataTable();
  });
  
  
  
  // Use jQuery to listen for the modal 'hidden' event
  $('#dispatchModal').on('hidden.bs.modal', function () {
    $('#DispatchForm')[0].reset();
  });
  