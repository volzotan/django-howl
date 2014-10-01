$(document).ready(function () {
    if ($("[rel=tooltip]").length) {
        $("[rel=tooltip]").tooltip();
    }

    // switching relays via ajax requests on links
    $(".ajaxbtn .btn").click(function(event) {
        event.preventDefault();
        $(".messagebox").empty();
        // ajax request for i.e. light/<name>/switch/on
        // response contains possible HTML with error-messages
        $(".messagebox").load(this.href); 
    });

});