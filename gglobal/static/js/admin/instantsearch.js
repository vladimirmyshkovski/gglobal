

    (function($) {
        $(document).ready(function($) {
            $('#changelist-search input[type=submit]').hide();
            $('label[for=searchbar]').html('Filter:');
            $('#searchbar').keyup(function(e) {
                if (e.keyCode === 27) {
                    if (!$(this).val()) {
                        return;
                    }
                    $(this).val('');
                }
                $('#changelist-form').load(window.location.pathname + '?q=' + $(this).val() + ' #changelist-form');
            }).focus();
        });
    })(django.jQuery);

