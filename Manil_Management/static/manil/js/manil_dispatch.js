$(document).ready(function () {
    $('#form-data-table').DataTable();
  });
    
  
    
    // Use jQuery to listen for the modal 'hidden' event
    $('#dispatchModal').on('hidden.bs.modal', function () {
      // Reset the form fields
      $('#DispatchForm')[0].reset();
    });
    