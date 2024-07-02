// Get the modal
var modal = document.getElementById("editModal");

// Get the button that opens the modal
var edit_button = document.getElementById("editButton");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
edit_button.onclick = function () {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    modal.style.display = "none";
}


// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {

}

document.getElementById('editPaperForm').addEventListener('submit', function (event) {
    event.preventDefault();
    console.log('submit');

    var formData = new FormData(this);

    fetch('/update-paper-detail', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Paper information uploaded successfully');
                $('#editModal').modal('hide');
            } else {
                // alert('File upload failed: ' + data.message);
            }
        }).catch(error => {
            console.error('Error:', error);
            // alert('An error occurred during the file upload');
        });
});