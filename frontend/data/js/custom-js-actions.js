$(window).resize(function () {
    $('.valign-wrapper-page').css({
        marginTop: ($(window).height() - $('.valign-wrapper-page').height()) / 2,
    });

});
// To initially run the function:
$(window).resize();

M.AutoInit();