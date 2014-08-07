(function(elem){ 
    elem.css("margin-top", Math.floor( ( $(window).height() / 2 ) - ( elem.height() / 2 ) ) );
}($("#loginWrap")));

$(window).resize(function(){
    $("#loginWrap").css("margin-top", Math.floor( ( $(window).height() / 2 ) - ( $("#loginWrap").height() / 2 ) ) );
  
});