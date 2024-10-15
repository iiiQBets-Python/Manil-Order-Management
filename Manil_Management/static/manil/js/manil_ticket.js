

$(document).ready(function () {
    $('#form-data-table').DataTable();
  });
  
  
  
  // Use jQuery to listen for the modal 'hidden' event
  $('#manil_ticketModal').on('hidden.bs.modal', function () {
    $('#TicketForm')[0].reset();
  });
  