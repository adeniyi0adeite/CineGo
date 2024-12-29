// video_stream.js


document.addEventListener("DOMContentLoaded", function() {
    const videoPlayer = document.getElementById("video-player");
    const paymentModal = new bootstrap.Modal(document.getElementById('paymentModal'));
    let freeWatchTime = {{ free_watch_time }};
    
    if (freeWatchTime === 0) return;  // User has full access, so don't limit the watch time

    let currentWatchTime = 0;

    videoPlayer.addEventListener('timeupdate', function() {
        currentWatchTime = videoPlayer.currentTime;
        let remainingTime = freeWatchTime - currentWatchTime;
        document.getElementById('remainingTime').innerText = Math.max(0, Math.floor(remainingTime));

        if (remainingTime <= 0) {
            videoPlayer.pause();
            paymentModal.show();
        }
    });
});



$(document).ready(function () {
    // Pay button click handler
    $('.pay-watch-btn').on('click', function () {
        var videoId = $(this).data('video-id');

        $.ajax({
            url: "{% url 'pay_per_watch_view' video_id=0 %}".replace('0', videoId),
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': '{{ csrf_token }}'
            },
            success: function (response) {
                if (response.success) {
                    // Redirect the user to Paystack's authorization URL
                    window.location.href = response.authorization_url;
                } else {
                    alert(response.error || 'An error occurred.');
                }
            },
            error: function () {
                alert('An error occurred. Please try again.');
            }
        });
    });

    // Payment form submission handler (e.g., after free watch time ends)
    $('#pay-per-watch-form').on('submit', function (e) {
        e.preventDefault();  // Prevent the default form submission
        var form = $(this);

        $.ajax({
            url: form.attr('action'),  // URL of the Paystack view
            type: 'POST',
            data: form.serialize(),  // Serialize form data including csrf_token
            success: function (response) {
                if (response.success) {
                    // Redirect the user to Paystack's authorization URL
                    window.location.href = response.authorization_url;
                } else {
                    alert(response.error || 'An error occurred while processing the payment.');
                }
            },
            error: function () {
                alert('An error occurred. Please try again.');
            }
        });
    });
});