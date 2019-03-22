$(function () {

    $(".btn-delete").click( function () {
        $(".btn-delete").hide();
        $("#btn-confirm").show();
        $("#btn-cancel-delete").show();
    });

    $("#btn-cancel-delete").click( function () {
      $(".btn-delete").show();
      $("#btn-confirm").hide();
      $("#btn-cancel-delete").hide();
    });
});
