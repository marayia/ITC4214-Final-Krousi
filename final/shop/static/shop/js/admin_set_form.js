// admin_set_form.js - scripts for the admin set form

$(document).ready(function() {
    // code: force uppercase as user types
    $('input[name="code"]').on('input', function() {
        $(this).val($(this).val().toUpperCase());
    });

    // slug: force lowercase, replace spaces with hyphens, strip invalid chars
    $('input[name="slug"]').on('input', function() {
        $(this).val($(this).val()
            .toLowerCase()
            .replace(/ /g, '-')
            .replace(/[^a-z0-9-]/g, '')
        );
    });

    // name: auto-generate slug from name if slug is empty
   // name: auto-generate slug if empty, and strip leading/trailing spaces
    $('input[name="name"]').on('blur', function() {
        $(this).val($.trim($(this).val()));
        var slug = $('input[name="slug"]');
        if (slug.val() === '') {
            slug.val($(this).val()
                .toLowerCase()
                .replace(/ /g, '-')
                .replace(/[^a-z0-9-]/g, '')
            );
        }
    });

});