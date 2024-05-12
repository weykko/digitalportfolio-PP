function initBootstrapForms() {
    $("form.bootstrap-form").find("input,textarea").addClass("form-control");
    $("form.bootstrap-form").find("input[type='submit']").removeClass("form-control");
}

function initCommenting(){
    $(".comment-input").on("keyup", function(event){
        var input = $(this);
        if(event.keyCode === 13) {
            var comment = $(this).val().trim();
            var post_id = $(this).data("post-id");
            if (comment.length > 0) {
                $.ajax("/post-comment/", {
                    data: {
                        post_id: post_id,
                        comment: comment
                    },
                    success: function(html){
                        $("#comments-list-post-"+post_id).append(html);
                        $(input).val("");
                    }
                })
            }
            return false;
        }
    })
}

$(document).ready(function(){
    initBootstrapForms();
    initCommenting();
});