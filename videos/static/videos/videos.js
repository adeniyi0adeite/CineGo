// videos/static/videos/videos.js

$(document).ready(function() {
    console.log("AJAX script is loaded and ready!");  // This will help you check if the file is linked

    $('#uploadButton').on('click', function(e) {
        e.preventDefault();

        var formData = new FormData($('#videoUploadForm')[0]);

        $.ajax({
            url: '/videos/upload/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log("Success!");  // Check if the success block is reached
                $('#successMessage').html(
                    '<div class="alert alert-success">Video uploaded successfully! Your link: ' + response.link + '</div>'
                );
                $('#errorMessage').html('');  // Clear error message
            },
            error: function(response) {
                console.log("Error!");  // Check if the error block is reached
                var error = response.responseJSON.error || 'An error occurred.';
                $('#errorMessage').html('<div class="alert alert-danger">' + error + '</div>');
            }
        });
    });
});
