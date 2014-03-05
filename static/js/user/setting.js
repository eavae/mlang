$(document).ready(function(){
    $("input[type=file]").change(function(){
        console.log($(this).val());
        $("#avatar-target").attr("src",$(this).val());
    });
});