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
  

$('#materialModal').on('hidden.bs.modal', function () {
  // Reset the form fields
  $('#MaterialForm')[0].reset();
});

var igst_rate = document.getElementById('igst_rate')
var cgst_rate = document.getElementById('cgst_rate')
var sgst_rate = document.getElementById('sgst_rate')

function validate_igst(){
  if (igst_rate.value){
    var new_val = Number(igst_rate.value)/2;

    cgst_rate.value = new_val;
    sgst_rate.value = new_val;
  } else{
    cgst_rate.value = null;
    sgst_rate.value = null;
  }
}

document.addEventListener('DOMContentLoaded', function () {
  if (igst_rate.value){
    validate_igst();
  }

});
  

