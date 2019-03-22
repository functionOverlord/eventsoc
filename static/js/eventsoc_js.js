$(function () {
    $(".btn-register-user").click( function () {
        $("#user-form").css("display", "inline");
        $(".register-buttons").hide();
    });

    $(".btn-register-society").click( function () {
        $("#society-form").css("display", "inline");
        $(".register-buttons").hide();
    });
});
