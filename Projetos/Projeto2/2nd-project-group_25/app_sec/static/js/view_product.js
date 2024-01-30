function showCommentForm() {
    var commentForm = document.getElementById("commentForm");
    commentForm.style.display = "block";

    var commentButton = document.getElementById("commentButton");
    commentButton.style.display = "none";

    var submitButton = document.getElementById("SubmitButton");
    submitButton.style.display = "block";

    var cancelButton = document.getElementById("CancelButton");
    cancelButton.style.display = "block";
}

function showCommentButton() {
    event.preventDefault(); // Evita o envio do formulário ao pressionar o botão Cancelar

    var cancelButton = document.getElementById("CancelButton");
    cancelButton.style.display = "none";

    var commentButton = document.getElementById("commentButton");
    commentButton.style.display = "block";

    var commentForm = document.getElementById("commentForm");
    commentForm.style.display = "none";

    var SubmitButton = document.getElementById("SubmitButton");
    SubmitButton.style.display = "none";
}

document.addEventListener('DOMContentLoaded', function() {
    var commentButton = document.getElementById('commentButton');
    if (commentButton) {
        commentButton.addEventListener('click', showCommentForm);
    }

    var cancelButton = document.getElementById('CancelButton');
    if (cancelButton) {
        cancelButton.addEventListener('click', showCommentButton);
    }
});
