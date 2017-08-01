$(document).ready(function() {
    $(".menu-button").on("click", function(){

        $(".menu-button").toggleClass("button-menu-open");
        $("body").toggleClass("menu-active");
        $("#menu").toggleClass("menu-expanded");
        $("#menu-open").toggleClass('hide');
        $("#menu-close").toggleClass('hide');
    });
});