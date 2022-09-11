$(document).on('submit', '.filter_form', function(e) {
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
            if("html_error" in response){
                document.querySelector("html").innerHTML = response["html_error"]
            }
            else{
                document.querySelector(".hide").classList.add('trans')
                setTimeout(() => {  
                    document.querySelector(".list").innerHTML = response["html"]
                }, 500);
                setTimeout(() => {  
                    document.querySelector(".hide").classList.remove('trans')
                }, 800); 
            }    
        }
    })
});
document.querySelector("html").addEventListener('click', function(e) {
    if(e.target.classList.contains("page-link")){
        e.preventDefault();
        var action_url = $(e.target).attr("href")
        formData = new FormData($('.filter_form').get(0));
        $.ajax({
            type: "POST",
            url: action_url,
            data: formData,
            contentType: false,
            processData: false,
            success: function(response){
                if("html_error" in response){
                    document.querySelector("html").innerHTML = response["html_error"]
                }
                else{
                    document.querySelector(".hide").classList.add('trans')
                    setTimeout(() => {  
                        document.querySelector(".list").innerHTML = response["html"]
                    }, 400);
                    setTimeout(() => {  
                        document.querySelector(".hide").classList.remove('trans')
                    }, 700); 
                }
            }
        })    
    }
})