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
                    var game = e.target.parentElement.parentElement
                    game.remove()
                }
            }
        })    
    }
})