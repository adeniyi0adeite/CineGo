$(document).ready(function() {
    $("#uploadButton").click(function() {
        // Form validation
        var isValid = validateForm();

        if (!isValid) {
            return;
        }

        // Get the form data
        var formData = new FormData($("#videoUploadForm")[0]);

        // Show the progress bar
        $(".progress").show();
        var progressBar = $("#progressBar");
        progressBar.css("width", "0%");
        progressBar.text("0%");

        // Send the AJAX request
        $.ajax({
            url: "/videos/upload/",
            type: "POST",
            data: formData,
            processData: false,  // Don't process the data
            contentType: false,  // Don't set content type
            xhr: function() {
                var xhr = new XMLHttpRequest();
                xhr.upload.onprogress = function(e) {
                    if (e.lengthComputable) {
                        var percent = (e.loaded / e.total) * 100;
                        progressBar.css("width", percent + "%");
                        progressBar.attr("aria-valuenow", percent);
                        progressBar.text(Math.round(percent) + "%");
                    }
                };
                return xhr;
            },
            success: function(response) {
                // On success, hide the progress bar and show success message
                $(".progress").hide();
                $("#successMessage").text(response.message).fadeIn();

                // Redirect to video list page
                setTimeout(function() {
                    window.location.href = "/videos/list/";
                }, 2000);
            },
            error: function(xhr, status, error) {
                // On error, hide progress bar and show error message
                $(".progress").hide();
                $("#errorMessage").text(xhr.responseJSON.error || 'An unexpected error occurred.').fadeIn();
            }
        });
    });

    // Validate form fields before submission
    function validateForm() {
        var isValid = true;

        // Validate title
        var title = $("#title");
        if (!title.val()) {
            title.addClass("is-invalid");
            isValid = false;
        } else {
            title.removeClass("is-invalid");
        }

        // Validate video file
        var videoFile = $("#video_file");
        if (!videoFile.val()) {
            videoFile.addClass("is-invalid");
            isValid = false;
        } else {
            videoFile.removeClass("is-invalid");
        }

        // Validate price
        var price = $("#price");
        if (!price.val() || parseFloat(price.val()) < 0) {
            price.addClass("is-invalid");
            isValid = false;
        } else {
            price.removeClass("is-invalid");
        }

        return isValid;
    }
});
