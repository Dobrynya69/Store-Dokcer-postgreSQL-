$(document).on('submit', '.comment_form', function(e) {
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
                document.querySelector(".list-group").classList.add("active")
                document.querySelector(".list-group").innerHTML = response["html"]
                setTimeout(() => {  
                    document.querySelector(".list-group").classList.remove("active")
                }, 400);
            }    
        }
    })
});
$(document).on('submit', '.comment_edit_form', function(e) {
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
            else if("html" in response){
                document.querySelector(".list-group").classList.add("active")
                document.querySelector(".list-group").innerHTML = response["html"]
                setTimeout(() => {  
                    document.querySelector(".list-group").classList.remove("active")
                }, 400);
            }    
        }
    })
});
document.querySelector("body").addEventListener('click', function(e) {
    if(e.target.classList.contains("comment-delete")){
        e.preventDefault();
        var action_url = $(e.target).attr("href")
        $.ajax({
            type: "GET",
            url: action_url,
            contentType: false,
            processData: false,
            success: function(response){
                if("html" in response){
                    document.querySelector(".list-group").classList.add("active")
                    document.querySelector(".list-group").innerHTML = response["html"]
                    setTimeout(() => {  
                        document.querySelector(".list-group").classList.remove("active")
                    }, 400);
                }
            }
        })    
    }
})
document.querySelector("body").addEventListener('click', function(e) {
    if(e.target.classList.contains("comment-edit")){
        var comment = e.target.parentElement.parentElement.parentElement
        for (let i = 0; i < comment.children.length; i++) {
            if(comment.children[i].classList.contains("comment_edit_form")){
                var all = document.querySelectorAll(".comment_edit_form")
                for (let j = 0; j < all.length; j++) {
                    all[j].classList.remove("active")
                }
                comment.children[i].classList.toggle("active")
            }
        }
    }
})
