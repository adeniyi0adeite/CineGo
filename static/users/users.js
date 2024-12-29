$(document).ready(function () {
    // General AJAX function
    function handleFormSubmit(formId, redirectUrl) {
        const form = $(formId);
        const url = form.attr('action');  // Dynamically get the form's action URL
        const formData = form.serialize();  // Serialize form data
        
        $.ajax({
            type: 'POST',
            url: url,  // Form action URL (it can be login or registration URL)
            data: formData,
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                if (response.success) {
                    $('#successMessage').html(`<div class="alert alert-success">${response.success}</div>`);
                    window.location.href = response.redirect || redirectUrl;  // Redirect if success
                }
            },
            error: function (xhr) {
                const response = JSON.parse(xhr.responseText);
                $('#errorMessage').html(`<div class="alert alert-danger">${response.error}</div>`);
            }
        });
    }

    // Bind form submit events
    $('#login-form').submit(function (e) {
        e.preventDefault();
        handleFormSubmit('#login-form', '/home');  // You can adjust the redirect URL as needed
    });

    $('#register-form').submit(function (e) {
        e.preventDefault();
        handleFormSubmit('#register-form', '/home');  // Adjust the redirect URL as needed
    });
});
