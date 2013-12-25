$(function () {
    var $link = $('.wrapper-inner_2').find('header').find('nav a');
    $link.click(function () {
        $link.removeClass("active");
        $(this).addClass("active");
    });
    
    $('a.hide-show').click(function(){
        par = $(this).parent();
        console.log(par);
        content = par.find('.content-container');
        console.log(content);
        if (content.hasClass('hide')) {
            content.removeClass('hide');
            $(this).text('Свернуть');
        }
        else {
            content.addClass('hide');
            $(this).text('Развернуть');
        };
    });
});
