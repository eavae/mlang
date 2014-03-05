$(document).ready(function (){
    $("#amend").wysiwyg({
        toolbarSelector:'[data-role=amend-toolbar]',
    });
    $("#explain").wysiwyg({
        toolbarSelector:' ',
    });
    $("#textarea-reply").wysiwyg({
        toolbarSelector:' ',
    });
    $(".textarea-a-reply").wysiwyg({
        toolbarSelector:' ',
    });

    $("#form-amend").submit(function (event){
        $(this).find("input[name=amend]").val($("#amend").html());
        $(this).find("input[name=explain]").val($("#explain").html());
        if($(this).find("#amend-count").val() > window.CONST.CHAR_MAX_LENGTH){
            return false;
        }
        if($(this).find("#explain-count").val() > window.CONST.CHAR_MAX_LENGTH){
            return false;
        }
    });
    //bind submit for comment box
    $("#form-comment").submit(function (event){
        $(this).find("input[name=comment]").val($("#textarea-reply").html());
        if($(this).find("#textarea-reply-count").val() > window.CONST.CHAR_MAX_LENGTH){
            return false;
        }
    });

    //bind click event on twitter-reply.
    $(".t-reply").each(function(){
        $(this).click(function(){
            var nick = $(this).attr('data-nick');
            var uid = $(this).attr('data-uid');
            var info = "@{'uid':'"+uid+"','nick':'"+nick+"'}";
            var _ = '<button name="'+info+'" onclick="return false;" contenteditable="false" unselectable="on" class="btn-textarea">To '+nick+':</button>&nbsp;';
            $("#textarea-reply").html(_).focus().setEndOfContenteditable().scrollGo();
            return false;
        });
    });

    //bind click event on amend-reply
    $(".a-reply").each(function(){
        $(this).click(function(){
            //show input box
            var nick = $(this).attr('data-nick');
            var uid = $(this).attr('data-uid');
            var aid = $(this).attr('data-aid');
            var info = "@{'uid':'"+uid+"','nick':'"+nick+"'}";
            $(".a-reply-box[data-aid="+aid+"]").show();
            var _ = '<button name="'+info+'" onclick="return false;" contenteditable="false" unselectable="on" class="btn-textarea">To '+nick+':</button>&nbsp;';
            $(".textarea-a-reply[data-aid="+aid+"]").html(_).focus().setEndOfContenteditable().scrollGo();
            return false;
        });
    });
    
    //bind form-amend-comment submit event
    $(".form-acomment").each(function(){
        $(this).submit(function (event){
            var aid = $(this).find("input[name=aid]").val();
            $(this).find("input[name=comment]").val($(".textarea-a-reply[data-aid="+aid+"]").html());
            if($(this).find("input#a-comment-count").val() > window.CONST.CHAR_MAX_LENGTH){
                return false;
            }
        });
    });
    //bind text reply event
    // $(".text").each(function(){
    //     $(this).mouseover(function(){
    //         $(this).find(".toolbar a").show();
    //     });
    //     $(this).mouseout(function(){
    //         $(this).find(".toolbar a").hide();
    //     });
    // });
});