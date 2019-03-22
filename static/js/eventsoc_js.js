$(function () {

    $(".btn-register-user").click( function () {
        $("#user-form").css("display", "inline");
        $(".register-buttons").hide();
        $("#header").hide();
    });

    $(".btn-register-society").click( function () {
        $("#society-form").css("display", "inline");
        $(".register-buttons").hide();
        $("#header").hide();
    });

    $("#about-btn").click( function(event) {
        alert("Email us at eventsoc@gu.gla.ac.uk");
        });
});
