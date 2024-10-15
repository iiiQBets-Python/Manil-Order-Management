
$(document).ready(function () {
    $('#form-data-table').DataTable();
  });
  
  
  
  // Use jQuery to listen for the modal 'hidden' event
  $('#userModal').on('hidden.bs.modal', function () {
    $('#UserForm')[0].reset();
  });
  