// admin_card_form.js - client-side validation for the card add/edit form

$(document).ready(function() {
    // price: cap at 99999 as user types
    $('input[name="price"]').on('input', function() {
        if ($(this).val() > 99999) {
            $(this).val(99999);
        }
        if ($(this).val() < 0) {
            $(this).val(0);
        }
    });

    // stock: cap at 999 as user types
    $('input[name="stock"]').on('input', function() {
        if ($(this).val() > 999) {
            $(this).val(999);
        }
        if ($(this).val() < 0) {
            $(this).val(0);
        }
    });

    // card number: only allow digits and /
    $('input[name="card_number"]').on('input', function() {
        $(this).val($(this).val().replace(/[^0-9/]/g, ''));
    });

    // name: strip leading/trailing spaces on blur
    $('input[name="name"]').on('blur', function() {
        $(this).val($.trim($(this).val()));
    });
});