/* Project specific Javascript goes here. */

/*
Formatting hack to get around crispy-forms unfortunate hardcoding
in helpers.FormHelper:

    if template_pack == 'bootstrap4':
        grid_colum_matcher = re.compile('\w*col-(xs|sm|md|lg|xl)-\d+\w*')
        using_grid_layout = (grid_colum_matcher.match(self.label_class) or
                             grid_colum_matcher.match(self.field_class))
        if using_grid_layout:
            items['using_grid_layout'] = True

Issues with the above approach:

1. Fragile: Assumes Bootstrap 4's API doesn't change (it does)
2. Unforgiving: Doesn't allow for any variation in template design
3. Really Unforgiving: No way to override this behavior
4. Undocumented: No mention in the documentation, or it's too hard for me to find
*/
$('.form-group').removeClass('row');

defer(function () {
	$('.phone-input-field').inputmask({"mask": "+375(99)999-99-99", "clearIncomplete": true}); 
});
                defer(function () {
                    $('.popup-video').magnificPopup({
                      disableOn: 700,
                      type: 'iframe',
                      mainClass: 'mfp-fade',
                      removalDelay: 160,
                      preloader: false,

                      fixedContentPos: false
                    });                
                })

            defer(function () {
                $('.popup-form').magnificPopup({
                    type: 'inline',
                    preloader: false,
                    focus: '.popup-form-name',
                    closeBtnInside: false, 
                    removalDelay: 300,

                    // When elemened is focused, some mobile browsers in some cases zoom in
                    // It looks not nice, so we disable it:
                    callbacks: {
                        beforeOpen: function() {
                            if($(window).width() < 700) {
                                this.st.focus = false;
                            } else {
                                this.st.focus = '.popup-form-name';
                            }
                        }
                    }
                });
            });
/*
                    defer(function () {
                    var phone;
                    var name;
                    var text;
                    $(".form-submit").click(function(e){
                        e.preventDefault();
                        var selfForm = $(this).parents('form:first');
                    

                    if($(selfForm)[0].checkValidity() == false){
                        if (selfForm[0].hasOwnProperty(['name'])) {
                            if ($(selfForm)[0]['name'].checkValidity() == false){
                                $(selfForm)[0]['name'].nextElementSibling.innerHTML = $(selfForm)[0]['name'].validationMessage;
                            }
                            name == selfForm[0]['name'].value}
                            else {name == null };

                        if (selfForm[0].hasOwnProperty(['phone'])) {
                            if ($(selfForm)[0]['phone'].checkValidity() == false){
                                $(selfForm)[0]['phone'].nextElementSibling.innerHTML= $(selfForm)[0]['phone'].validationMessage;
                            }
                            phone == selfForm[0]['phone'].value}
                            else {phone == null };

                        if (selfForm[0].hasOwnProperty(['text'])) {
                            if ($(selfForm)[0]['text'].checkValidity() == false){
                                $(selfForm)[0]['text'].nextElementSibling.innerHTML = $(selfForm)[0]['text'].validationMessage;
                            }
                            text == selfForm[0]['text'].value}
                            else {text == null };
                    } 
                    else {
                        jQuery.ajax({type: 'POST',
                                dataType: 'json',
                                async: true,
                                url: '',
                                data: { 'csrfmiddlewaretoken': csrftoken,
                                name: name,
                                phone: phone,
                                text: text,
                                form: selfForm[0].id,
                            },
                            success: setTimeout(function(data) { 
                                $.magnificPopup.open({ 
                                    items: { 
                                        src: '#thank-you-modal', 
                                        type: 'inline' 
                                    } 
                                });
                                $('.name-input-field').val(''), 
                                $('.phone-input-field').val('') 
                            }, 1000), 
                            error: function(xhr, textStatus) { 
                                $.magnificPopup.open({ 
                                    items: { 
                                        src: '#error-modal', 
                                        type: 'inline', 
                                    } 
                                });
                            }
                        });
                    }
                    return false;
                });
        });
*/