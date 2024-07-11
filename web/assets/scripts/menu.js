$(document).ready(function() {

    $('.header__menu-item').each( function() {
        if($(this).attr('href') === window.location.pathname) {
            $(this).addClass('header__menu-item_active')
        }
    });

});