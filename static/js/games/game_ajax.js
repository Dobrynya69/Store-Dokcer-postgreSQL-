$(document).on('submit', '.grade_form', function(e) {
    e.preventDefault();
    var action_url = $(this).attr("action")
    formData = new FormData($(this).get(0));
    $.ajax({
        type: "POST",
        url: action_url,
        data: formData,
        contentType: false,
        processData: false,
        success: function(response){
            if("html" in response){
                document.querySelector("game").innerHTML = response["html"]
            }
            else if("form_error" in response){
                document.querySelector(".form_error").innerHTML = response["form_error"]
            }    
        }
    })
});