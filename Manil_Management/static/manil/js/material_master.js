// Jquery datatables script
$(document).ready(function () {
  $('#form_data_table').DataTable();
});
  
$(document).ready(function() {
  // Check if DataTable is already initialized to avoid reinitialization
  if ($.fn.DataTable.isDataTable('#form-data-table')) {
      // Destroy the existing DataTable before re-initializing
      $('#form-data-table').DataTable().destroy();
  }

  // Initialize the DataTable again
  $('#form-data-table').DataTable({
      "columnDefs": [
          { "orderable": false, "targets": 6 } // Disable sorting for the "Action" column
      ],
      "order": [] // Disable default sorting on any column
   });
});
  
// Use jQuery to listen for the modal 'hidden' event
$('#materialModal').on('hidden.bs.modal', function () {
  // Reset the form fields
  $('#MaterialForm')[0].reset();
});
  