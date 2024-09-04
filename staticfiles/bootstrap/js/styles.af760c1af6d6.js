$(document).ready(function() {
    var lastScrollTop = 0;
    $(window).scroll(function(event) {
        var st = $(this).scrollTop();
        if (st > lastScrollTop) {
            // Scroll down
            $('.navbar').addClass('navbar-hide');
        } else {
            // Scroll up
            $('.navbar').removeClass('navbar-hide');
        }
        lastScrollTop = st;
    });

    $('.navbar-nav .nav-item .nav-link').on('click', function() {
        $('.navbar-nav .nav-item .nav-link').removeClass('active');
        $(this).addClass('active');
    });``
});

