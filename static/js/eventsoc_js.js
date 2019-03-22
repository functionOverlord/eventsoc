$(function () {

    $(".btn-register-user").click(function () {
        $("#user-form").css("display", "inline");
        $(".register-buttons").hide();
    });

    $(".btn-register-society").click(function () {
        $("#society-form").css("display", "inline");
        $(".register-buttons").hide();
    });

    $("#about-btn").click(function (event) {
        alert("Email us at eventsoc@gu.gla.ac.uk");
    });

    $(".register-back").click(function () {
        $(".register-form").hide();
        $(".register-buttons").css("display", "inline");
    });


    // hide bookmark hearts from booked and bookmarked pages from event cards
    $(".bookmarked-page .float").hide();
    $(".booked-page .float").hide();
});
