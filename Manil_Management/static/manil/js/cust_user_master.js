// Jquery datatables script


$(document).ready(function () {
    $('#form-data-table').DataTable();
  });
  
  
  
  // Use jQuery to listen for the modal 'hidden' event
  $('#cust_userModel').on('hidden.bs.modal', function () {  
    $('#ClientForm')[0].reset();
  });
  