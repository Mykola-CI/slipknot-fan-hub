$(document).ready(function () {
    $('.edit-btn').click(function () {
        var formType = $(this).data('form');
        $('#modal-form').data('form_type', formType);
        $.ajax({
            url: profileUrl,
            type: 'GET',
            data: { 'form_type': formType },
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            success: function (response) {
                // Replace the content of the form-fields div with the response
                $('#form-fields').html(response);
                $('#modal').show();
            },
            error: function (xhr, status, error) {
                console.error("Error fetching form: " + error);
            }
        });
    });

    $('.close').click(function () {
        $('#modal').hide();
    });

    $('#modal-form').submit(function(e) {
        e.preventDefault();
        var formData = new FormData(this);
    
        // Append CSRF token to FormData
        var csrftoken = $('[name=csrfmiddlewaretoken]').val(); // Get the CSRF token from a hidden input
        formData.append('csrfmiddlewaretoken', csrftoken);

        // Append form type to FormData
        var formType = $('#modal-form').data('form_type');
        formData.append('form_type', formType);

        $.ajax({
            url: profileUrl,
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            headers: {'X-Requested-With': 'XMLHttpRequest'},
            success: function(response) {
                if (response.status === 'success') {
                    location.reload();
                } else {
                    alert('Error: ' + JSON.stringify(response.errors));
                }
            },
            error: function(xhr, status, error) {
                alert('An error occurred: ' + error);
            }
        });
    });    
});
