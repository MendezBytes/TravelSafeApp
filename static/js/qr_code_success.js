$(document).ready(function () {

    $("#printButton").click((e) => {

        qr_code_url = $("#printButton").attr("data-qrcode")
        newWindow = window.open(qr_code_url);
        newWindow.print();
    })
});
