document.addEventListener("DOMContentLoaded", function() {
    const editButtons = document.querySelectorAll(".btn-edit");
    const commentText = document.querySelector("#id_content");
    const commentForm = document.querySelector("#commentForm");
    const submitButton = document.querySelector("#submitButton");
    const discardChanges = document.querySelector("#discardChanges");
    const modalCommentDelete = document.querySelector("#modalCommentDelete");
    const deleteButtons = document.querySelectorAll(".btn-delete");
    const deleteConfirm = document.querySelector("#deleteConfirm");
    const closeModalButton = modalCommentDelete.querySelector(".close");

    editButtons.forEach(button => {
        button.addEventListener("click", (e) => {
            let commentId = e.target.getAttribute("data-comment_id");
            let commentContent = document.querySelector(`#comment${commentId}`).innerText;
            let formTitle = document.querySelector("#formTitle");
            commentText.value = commentContent;
            submitButton.innerText = "Save Changes";
            formTitle.innerText = "Edit Comment";
            discardChanges.classList.remove("hidden");
            commentForm.action = `edit_comment/${commentId}`;
        });
    });

    closeModalButton.addEventListener("click", () => {
        modalCommentDelete.classList.remove("show");
    });

    deleteButtons.forEach(button => {
        button.addEventListener("click", (e) => {
            let commentId = e.target.getAttribute("data-comment_id");
            deleteConfirm.href = `delete_comment/${commentId}`;
            modalCommentDelete.classList.add("show");
        });
    });

    window.addEventListener("click", (e) => {
        if (e.target === modalCommentDelete) {
            modalCommentDelete.classList.remove("show");
        }
    });
});
