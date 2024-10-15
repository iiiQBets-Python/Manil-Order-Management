

$(document).ready(function () {
    $('#form-data-table').DataTable();
  });
  
  
  
  // Use jQuery to listen for the modal 'hidden' event
  $('#chaipointModal').on('hidden.bs.modal', function () {
    $('#ChaipointForm')[0].reset();
  });
  