$(document).ready(function (){
    //automatically fill the language select list
    var select_html = "";
    for (var i = 0; i < window.CONST.LANG.length; i++) {
        select_html += '<option value="'+window.CONST.LANG[i][0]+'">'+window.CONST.LANG[i][1]+'</option>';
    }
    $("select[name=language]").html(select_html);

    $("#t-content").wysiwyg();

    $("form#form-t-new").submit(function(event){
        $(this).find("input[name=content]").val($("#t-content").html());
        if($(this).find("input[name=t-content-count]").val() > window.CONST.CHAR_MAX_LENGTH)
            return false;
    });
    //text hover event

    // $(".text").each(function(){
    //     $(this).mouseover(function(){
    //         $(this).find(".toolbar a").show();
    //     });
    //     $(this).mouseout(function(){
    //         $(this).find(".toolbar a").hide();
    //     });
    // });
});