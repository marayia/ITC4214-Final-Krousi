// rating.js - AJAX star rating for card detail page

$(document).ready(function() {
    const stars = $('.tt-star');
    const ratingInfo = $('#rating-info');
    const ratingUrl = $('.tt-rating').data('url');
    // hover effect
    stars.on('mouseenter', function() {
        const val = $(this).data('value');
        stars.each(function() {
            $(this).toggleClass('hover', $(this).data('value') <= val);
        });
    });

    stars.on('mouseleave', function() {
        stars.removeClass('hover');
    });

    // click to rate
    stars.on('click', function() {
        const val = $(this).data('value');
        const csrfToken = $('[name=csrfmiddlewaretoken]').val();

        $.ajax({
            url: ratingUrl,
            method: 'POST',
            data: { stars: val, csrfmiddlewaretoken: csrfToken },
            success: function(data) {
                // update stars display
                stars.each(function() {
                    $(this).toggleClass('active', $(this).data('value') <= data.user_rating);
                });
                // update rating info
                ratingInfo.text(data.average + '/5 (' + data.count + ' rating' + (data.count !== 1 ? 's' : '') + ')');
            }
        });
    });
});