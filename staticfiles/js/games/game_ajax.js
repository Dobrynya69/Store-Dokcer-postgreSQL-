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
document.querySelector("body").addEventListener('click', function(e) {
    if(e.target.classList.contains("favorite-button")){
        e.preventDefault();
        var action_url = $(e.target).attr("href")
        $.ajax({
            type: "GET",
            url: action_url,
            contentType: false,
            processData: false,
            success: function(response){
                if("success" in response){
                    if (response["success"] == 'Create') {
                        e.target.classList.remove("btn-success")
                        e.target.classList.add("btn-danger")
                        e.target.innerHTML = "Remove favorite-"
                    }
                    else if (response["success"] == 'Delete') {
                        e.target.classList.remove("btn-danger")
                        e.target.classList.add("btn-success")
                        e.target.innerHTML = "Add favorite+"
                    }
                }
            }
        })    
    }
})