$(document).ready(function () {
  $('#form-data-table').DataTable();
});



// Use jQuery to listen for the modal 'hidden' event
$('#orderModal').on('hidden.bs.modal', function () {
  // Reset the form fields
  $('#OrderForm')[0].reset();
});




document.addEventListener('DOMContentLoaded', function () {

  const orderDetailsContainer = document.querySelector('.order-details-container');

  // Add new section
  orderDetailsContainer.addEventListener('click', function (e) {
    if (e.target.closest('.add-more')) {
      e.preventDefault(); // Prevent default action
      e.stopImmediatePropagation(); // Prevent multiple event triggers

      const orderDetailRow = e.target.closest('.order-details-row'); // Target the row to clone
      const clone = orderDetailRow.cloneNode(true); // Clone the entire row
      resetFormFields(clone); // Optional: reset fields in cloned section

      // Increment the suffix for ids, names, and labels in the cloned section
      updateIdsNamesAndLabels(clone, orderDetailsContainer.querySelectorAll('.order-details-row').length + 1);

      // Add both "Remove" and "Add More" buttons to the last (new) section
      clone.querySelector('.col-lg-1').innerHTML = `
        <button type="button" class="btn btn-sm btn-success add-more">
          <i class="fas fa-plus"></i>
        </button>
        <button type="button" class="btn btn-sm btn-danger remove-section">
          <i class="fas fa-trash"></i>
        </button>
      `;

      orderDetailsContainer.appendChild(clone); // Append the cloned row

      document.getElementById('no_of_sec').value = orderDetailsContainer.querySelectorAll('.order-details-row').length;

      console.log('no_of_sec_add', document.getElementById('no_of_sec').value)

      updateButtonsVisibility();
    }
  });

  // Remove section and adjust the remaining section numbers
  orderDetailsContainer.addEventListener('click', function (e) {
    if (e.target.closest('.remove-section')) {
      const orderDetailRow = e.target.closest('.order-details-row'); // Target the row to remove
      if (orderDetailsContainer.querySelectorAll('.order-details-row').length > 1) {
        orderDetailRow.remove(); // Remove the row
        adjustSectionNumbers(); // Adjust section numbers after deletion
        updateButtonsVisibility(); // Update button visibility after deletion
      } else {
        alert('At least one order detail section is required.');
      }

      document.getElementById('no_of_sec').value = orderDetailsContainer.querySelectorAll('.order-details-row').length;

      console.log('no_of_sec_remove', document.getElementById('no_of_sec').value)
    }
  });

  // Function to reset input fields in cloned section
  function resetFormFields(clone) {
    const inputs = clone.querySelectorAll('input, select');
    inputs.forEach(input => {
      if (!input.id.startsWith('gst_type')) { // Skip inputs with ids starting with "gst_type"
        input.value = ''; // Clear input and select values
      }
    });
  }

  // Function to update ids, names, and labels in the cloned section
  function updateIdsNamesAndLabels(clone, sectionNumber) {
    const allInputs = clone.querySelectorAll('input, select'); // Get all input and select fields
    const allLabels = clone.querySelectorAll('label'); // Get all label elements

    // Update ids and names for input and select elements
    allInputs.forEach(input => {
      const id = input.id;
      const name = input.name;

      if (id) {
        const newId = id.replace(/\d+$/, sectionNumber); // Update the id suffix
        input.id = newId;

        // Update the event handlers based on the new suffix
        if (id.startsWith('material_name_')) {
          input.setAttribute('onchange', `handle_material(${sectionNumber})`);
        }
        if (id.startsWith('qty_')) {
          input.setAttribute('oninput', `subtotal_cal(${sectionNumber})`);
        }
      }

      if (name) {
        const newName = name.replace(/\d+$/, sectionNumber); // Update the name suffix
        input.name = newName;
      }
    });

    // Update the "for" attribute in the label elements
    allLabels.forEach(label => {
      const labelFor = label.getAttribute('for');

      if (labelFor) {
        const newLabelFor = labelFor.replace(/\d+$/, sectionNumber); // Update the "for" attribute suffix
        label.setAttribute('for', newLabelFor);
      }
    });
    calculateGrandTotal();
  }

  // Function to adjust section numbers after deletion
  function adjustSectionNumbers() {
    const allSections = orderDetailsContainer.querySelectorAll('.order-details-row');

    allSections.forEach((section, index) => {
      const newSectionNumber = index + 1; // New section number (starting from 1)
      updateIdsNamesAndLabels(section, newSectionNumber); // Update the ids, names, and labels
    });
  }

  // Function to update button visibility for each section
  function updateButtonsVisibility() {
    const allSections = orderDetailsContainer.querySelectorAll('.order-details-row');

    // Iterate through all sections to adjust button visibility
    allSections.forEach((section, index) => {
      const addMoreButton = section.querySelector('.add-more');
      const removeSectionButton = section.querySelector('.remove-section');

      // First section (_1) should not have Remove or Add More button (only initially)
      if (index === 0) {
        if (removeSectionButton) removeSectionButton.remove();
        if (addMoreButton && allSections.length === 1) {
          // Add More button only appears in first section when it's the only section
          addMoreButton.style.display = 'inline-block';
        } else if (addMoreButton) {
          addMoreButton.style.display = 'none';
        }
      }

      // Last section should have both Add More and Remove button
      else if (index === allSections.length - 1) {
        if (!addMoreButton) {
          section.querySelector('.col-lg-1').innerHTML += `
            <button type="button" class="btn btn-sm btn-success add-more">
              <i class="fas fa-plus"></i>
            </button>`;
        }
        if (!removeSectionButton) {
          section.querySelector('.col-lg-1').innerHTML += `
            <button type="button" class="btn btn-sm btn-danger remove-section">
              <i class="fas fa-trash"></i>
            </button>`;
        }
      }

      // All other sections should only have the Remove button
      else {
        if (addMoreButton) addMoreButton.remove();
        if (!removeSectionButton) {
          section.querySelector('.col-lg-1').innerHTML += `
            <button type="button" class="btn btn-sm btn-danger remove-section">
              <i class="fas fa-trash"></i>
            </button>`;
        }
      }
    });
  }

  // Call the function initially to ensure correct button visibility
  updateButtonsVisibility();

});



function numberToWords(num) {
  const ones = [
    '', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
    'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen',
    'Seventeen', 'Eighteen', 'Nineteen'
  ];

  const tens = [
    '', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety'
  ];

  const thousands = [
    '', 'Thousand', 'Million', 'Billion'
  ];

  if (num === 0) return 'Zero';

  let words = '';
  let i = 0;

  while (num > 0) {
    let chunk = num % 1000;
    if (chunk) {
      let str = '';
      if (chunk % 100 < 20) {
        str = ones[chunk % 100];
        chunk = Math.floor(chunk / 100);
      } else {
        str = ones[chunk % 10];
        chunk = Math.floor(chunk / 10);
        str = tens[chunk % 10] + (str ? ' ' + str : '');
        chunk = Math.floor(chunk / 10);
      }
      if (chunk) {
        str = ones[chunk] + ' Hundred' + (str ? ' and ' + str : '');
      }
      words = str + (thousands[i] ? ' ' + thousands[i] : '') + ' ' + words;
    }
    num = Math.floor(num / 1000);
    i++;
  }

  return words.trim();
}

function calculateGrandTotal() {
  var grandTotal = 0;
  var i = 1;

  while (document.getElementById(`sub_total_${i}`) !== null) {
    var subTotalValue = document.getElementById(`sub_total_${i}`).value;
    grandTotal += Number(subTotalValue) || 0;
    i++;
  }

  grandTotal = Math.round(grandTotal);

  document.getElementById('grand_total').value = grandTotal;

  var grandTotalInWords = numberToWords(Math.floor(grandTotal));
  document.getElementById('amt_in_words').value = grandTotalInWords + ' Rupees Only';
}



function subtotal_cal(value) {

  var quantity = document.getElementById(`qty_${value}`);
  var baseprice = document.getElementById(`base_price_${value}`);
  var gstrate = document.getElementById(`gst_rate_${value}`);


  var gstamt = document.getElementById(`gst_amt_${value}`);
  var subtotal = document.getElementById(`sub_total_${value}`);


  if (baseprice.value && gstrate.value) {
    var gstAmountForOne = (Number(gstrate.value) / 100) * Number(baseprice.value)* Number(quantity.value);
    gstAmountForOne = (gstAmountForOne.toString().includes('.') && gstAmountForOne.toString().split('.')[1].length > 3)
      ? gstAmountForOne.toFixed(3)
      : gstAmountForOne;
    gstamt.value = gstAmountForOne;
  }


  if (quantity.value && baseprice.value && gstrate.value) {

    var gstAmountForOne = (Number(gstrate.value) / 100) * Number(baseprice.value);
    var priceIncludingGST = Number(baseprice.value) + gstAmountForOne;
    var totalAmount = priceIncludingGST * Number(quantity.value);

    subtotal.value = totalAmount;
  } else {
    subtotal.value = null;
  }

  calculateGrandTotal();

}



function handle_material(value) {
  var mat_inp = document.getElementById(`material_name_${value}`);
  var selectedOption = mat_inp.options[mat_inp.selectedIndex];
  var mat_uom = selectedOption.getAttribute('uom');
  var baseprince = selectedOption.getAttribute('base_prince');

  var c_gst = selectedOption.getAttribute('cgst');
  var s_gst = selectedOption.getAttribute('sgst');
  var i_gst = selectedOption.getAttribute('igst');
  
  var hsn_code = selectedOption.getAttribute('hsn_code');


  if (in_side) {
    document.getElementById(`gst_rate_${value}`).value = Number(c_gst) + Number(s_gst);
  } else {
    document.getElementById(`gst_rate_${value}`).value = Number(i_gst);
  }


  if (mat_uom) {
    document.getElementById(`uom_${value}`).value = mat_uom;
  } else {
    document.getElementById(`uom_${value}`).value = null;
  }

  if (baseprince) {
    document.getElementById(`base_price_${value}`).value = baseprince;
  } else {
    document.getElementById(`base_price_${value}`).value = null;
  }

  if (hsn_code) {
    document.getElementById(`hsn_code_${value}`).value = hsn_code;
  } else {
    document.getElementById(`hsn_code_${value}`).value = null;
  }

  subtotal_cal(value);
}

