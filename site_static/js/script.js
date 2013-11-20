$(function () {
    var $link = $('.wrapper-inner_2').find('header').find('nav a');
    $link.click(function () {
        $link.removeClass("active");
        $(this).addClass("active");
    });
});