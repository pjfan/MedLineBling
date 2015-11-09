
$(document).ready(function(){
    
    $("#search").click(function(){
        var $value = $("#textarea").val();
        window.alert($value);
        $("#searchable_wrapper").animate({marginRight: "70%"});
        $("#searchable").prepend("<div id=content>fdfd</div>");
        
    });
    
    
});