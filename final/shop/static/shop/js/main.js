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