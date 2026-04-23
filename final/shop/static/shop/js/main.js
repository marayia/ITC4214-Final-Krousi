// toggle the search bar below the navbar when the search icon is tapped on mobile
$(document).ready(function () {
    $('#mobile-search-toggle').on('click', function () {
        $('#mobile-search').slideToggle(200, function () {
            if ($(this).is(':visible')) {
                $('#mobile-search-input').focus();
            }
        });
    });
});

$(document).ready(function() {
    // apply header color from data attribute
    const header = $('.profile-header[data-color]');
    if (header.length) {
        header.css('background', header.data('color'));
    }

    // color swatch selection highlight
    $('input[name="header_color"]').on('change', function() {
        $('input[name="header_color"]').each(function() {
            $(this).next('.color-swatch').css('border-color', 'transparent');
        });
        $(this).next('.color-swatch').css('border-color', 'white');
    });
});