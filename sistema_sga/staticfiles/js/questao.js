$(function () {
    $("#frm-answers input[type=radio]").click(function () {
        var answer = $(this).val();
        $.ajax({
            url: '/prova/send-response/',
            data: $('#frm-answers').serialize(),
            type: 'post',
            cache: false,
            success: function () {
	          $("#result").slideDown(1000).show(0).delay(2000).slideUp(1000).hide(0);
              $("input").prop('disabled', true);
	        }
        });
    });
});