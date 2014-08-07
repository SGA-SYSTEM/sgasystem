$(function(){
  /*$("body").before("<h1 align='center'>jQuery</h1>");*/
  
  $("input[name=button]").click(function(){
    var login = $("input[name=login]").val();
      var pass =   $("input[name=pass]").val();
      if (login=="" || pass=="")
        throw_message("Insira os dados corretamente!");
      else
        throw_message("Carregando...");
  });

});

function throw_message(str) {
        $('#error_box').html(str).fadeIn(500).delay(3000).fadeOut(500);
}