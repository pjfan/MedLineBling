
$(document).ready(function(){
    $("#search").click(function(){
        /*Retrieves value from the search bar*/
        var $value = $("#textarea").val();
        /*Moves the logo and search bar to the left side of the screen.*/
        $("#searchable_wrapper").animate({marginRight: "70%"});
        /*Sends a get request to the flask server $SCRIPT_ROOT is defined in the index.html file.*/
        $.getJSON($SCRIPT_ROOT + '/drug', {
            medlinesearch: $value
            }, function(data) {
                /*This function grabs values from the returned JSON, adds in html tags and prepends them to the #searchable div in index.html.*/
                var $prependhtml = "<div id=content><h1>Effects of "+data.drug+"</h1><p>"+data.definition+"<p><h4>Similar Drugs</h4><table>";
                $.each(data.others, function(index,val){
                    $prependhtml += "<tr><td>"+val+"</td></tr>"
                });
                $prependhtml += "</table></div>";
                $("#searchable").prepend($prependhtml);
            });
        return false;
    });          
});