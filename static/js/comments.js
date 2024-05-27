document.addEventListener("DOMContentLoaded", function() {
    const editButtons = document.querySelectorAll(".btn-edit");
    const commentText = document.querySelector("#id_content");
    const commentForm = document.querySelector("#commentForm");
    const submitButton = document.querySelector("#submitButton");

    editButtons.forEach(button => {
        button.addEventListener("click", (e) => {
            let commentId = e.target.getAttribute("data-comment_id");
            let commentContent = document.querySelector(`#comment${commentId}`).innerText;
            commentText.value = commentContent;
            submitButton.innerText = "Save Changes";
            commentForm.action = `edit_comment/${commentId}`;
        });
    });
});