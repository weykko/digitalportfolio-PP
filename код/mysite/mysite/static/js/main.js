document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.like-btn');

    likeButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const postId = this.getAttribute('data-id');
            let likeCountElement = this.querySelector('.like-count');

            fetch(`/post/${postId}/like/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Получение токена CSRF
                }
            })
            .then(response => response.json())
            .then(data => {
                likeCountElement.textContent = data.total_likes;
            })
            .catch(error => console.error('Error:', error));
        });
    });
});

// Функция для получения значения CSRF токена из куки
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Проверим соответствует ли строка нашему имени
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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