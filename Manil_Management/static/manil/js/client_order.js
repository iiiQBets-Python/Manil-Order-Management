$(document).ready(function () {
  $('#form-data-table').DataTable();
});
  

  
  // Use jQuery to listen for the modal 'hidden' event
  $('#orderModal').on('hidden.bs.modal', function () {
    // Reset the form fields
    $('#OrderForm')[0].reset();
  });
  