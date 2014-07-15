$(function () {
    $("#frm-answers input[type=radio]").click(function () {
        var answer = $(this).val();
        $.ajax({
            url: '/prova/send-response/',
            data: $('#frm-answers').serialize(),
            type: 'post',
            cache: false
        });
    });
});