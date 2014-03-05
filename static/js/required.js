$(document).ready(function () {
    //automatically fill the language select list
    var select_html = "";
    //<option value="zh_CN">chinese</option>
    for (var i = 0; i < window.CONST.LANG.length; i++) {
        select_html += '<option value="'+window.CONST.LANG[i][0]+'">'+window.CONST.LANG[i][1]+'</option>';
    }
    $("select[name=native]").html(select_html);
    $("select[name=learning]").html(select_html);
});