function enableForm() {
    const inputs = document.querySelectorAll('.editable-input');
    inputs.forEach(input => {
        if (input.hasAttribute('readonly')) {
            input.classList.remove('active');
            input.classList.add('inactive'); // Add inactive class when readonly
        } else {
            input.classList.remove('inactive');
            input.classList.add('active'); // Add active class when editable
        }
        input.removeAttribute('readonly'); // Make inputs editable
    });

    // Show save button and hide edit button
    document.getElementById('edit_1').style.display = 'none';
    document.getElementById('submit_1').style.display = 'inline-block';
}
