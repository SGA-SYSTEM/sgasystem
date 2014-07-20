$(function () {
    $("#frm-answers input[type=radio]").click(function () {
        var answer = $(this).val();
        $.ajax({
            url: '/prova/send-response/',
            data: $('#frm-answers').serialize(),
            type: 'post',
            cache: false,
            beforeSend: function () {
	          var html = "<p class='alert alert-warning' style='text-align: center;'>Resposta enviada com sucesso!</p>"
              $('#alert').html(html);
              $("input").prop('disabled', true);
	        }
        });
    });
});