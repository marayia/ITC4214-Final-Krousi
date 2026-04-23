// main.js - global scripts loaded on every page

$(document).ready(function() {
    // toggle the search bar below the navbar when the search icon is tapped on mobile
    $('#mobile-search-toggle').on('click', function() {
        $('#mobile-search').slideToggle(200, function() {
            if ($(this).is(':visible')) {
                $('#mobile-search-input').focus();
            }
        });
    });

    // apply header color from data attribute on profile pages
    const header = $('.profile-header[data-color]');
    if (header.length) {
        header.css('background', header.data('color'));
    }

    // color swatch selection — highlight selected swatch with white border
    $('input[name="header_color"]').on('change', function() {
        $('input[name="header_color"]').each(function() {
            $(this).next('.color-swatch').css('border-color', 'transparent');
        });
        $(this).next('.color-swatch').css('border-color', 'white');
    });
});