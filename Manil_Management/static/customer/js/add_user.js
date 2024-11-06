// Jquery datatables script


$(document).ready(function () {
    $('#form-data-table').DataTable();
  });
  
  
  
  // Use jQuery to listen for the modal 'hidden' event
  $('#add_userModel').on('hidden.bs.modal', function () {  
    $('#UserForm')[0].reset();
  });
  