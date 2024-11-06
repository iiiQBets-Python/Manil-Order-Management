// Jquery datatables script


$(document).ready(function () {
    $('#form-data-table').DataTable();
  });
  
  
  
  // Use jQuery to listen for the modal 'hidden' event
  $('#cust_userModel').on('hidden.bs.modal', function () {  
    $('#Client_userForm')[0].reset();
  });
  