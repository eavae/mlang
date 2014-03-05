window.CONST = {};

window.CONST.CHAR_MAX_LENGTH = 300;

$.fn.setCursorPosition = function (pos) {
    this.each(function (index, elem) {
        if (elem.setSelectionRange) {
            elem.setSelectionRange(pos, pos);
        } else if (elem.createTextRange) {
            var range = elem.createTextRange();
            range.collapse(true);
            range.moveEnd('character', pos);
            range.moveStart('character', pos);
            range.select();
        }
    });
    return this;
};

$.fn.setEndOfContenteditable = function()
{
    this.each(function(index,elem){
        var range,selection;
        if(document.createRange)//Firefox, Chrome, Opera, Safari, IE 9+
        {
            range = document.createRange();
            range.selectNodeContents(elem);
            range.collapse(false);
            selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange(range);
        }
        else if(document.selection)//IE 8 and lower
        {
            range = document.body.createTextRange();
            range.moveToElementText(elem);
            range.collapse(false);
            range.select();
        }
    });
    return this;
};

var globalWarningShow = function(msg){
    $(".global-alert-c").html('<div class="center-block alert alert-danger"style="max-width:700px;"><p><strong>Error: </strong>'+msg+'</p></div>');
    $(".global-alert-c > *").delay(3*1000).fadeOut('slow',function (){
        $(".global-alert-c").html('');
    });
};

$.fn.scrollGo = function() {
   var x = this.offset().top - 200;
   $('html,body').animate({scrollTop: x}, 500);
   return this;
};

$(document).ready(function (){
    $(".global-alert-c > *").delay(3*1000).fadeOut('slow',function (){
        $(".global-alert-c").html('');
    });
    //url match
    function stripTrailingSlash(str) {
        if(str.substr(-1) == '/') {
          return str.substr(0, str.length - 1);
        }
        return str;
    }
    var url = window.location.pathname;
    var activePage = stripTrailingSlash(url);
    $('#main-nav li a').each(function(){
        var currentPage = stripTrailingSlash($(this).attr('href'));
        if (activePage == currentPage){
            $(this).parent().addClass('active');
        }
    });
    //login control
    // var showUserInfo = function(){
    //     $("form#sign").hide();
    //     $("form#user").show();
    //     $("form#user button:first").html($.user.nickname);
    // };

    // $( "form#sign" ).on("submit", function(event) {
    //     var email = $(this).find("input[name=email]");
    //     var password = $(this).find("input[name=password]");
    //     var enableForm = function (){
    //         $("form input").attr("disabled", false);
    //         $("form button").attr("disabled", false);
    //     };
    //     var globalWarningHide = function(){
    //         $(".global-alert-c").html('');
    //     };
    //     $("form input").attr("disabled", true);
    //     $("form button").attr("disabled", true);
    //     $.ajax({
    //         type:"POST",
    //         url:"/j/login",
    //         data:{email:email.val(),password:password.val()},
    //     }).done(function (o){
    //         if (o.errors){
    //             for(var error in o.errors){
    //                 globalWarningShow(o.errors[error]);
    //             }
    //         }
    //         if(o.data){
    //             $.user = {};
    //             $.user.email = o.data.email;
    //             $.user.uid = o.data.uid;
    //             $.user.nickname = o.data.nickname;
    //             showUserInfo();
    //         }
    //         enableForm();
    //     }).fail(function (){
    //         //TODO:show error info
    //         enableForm();
    //     });
    //     return false;
    // });

    //other
});