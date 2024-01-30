function setDescription() {
    let textarea = document.getElementById('description');
    if (textarea) {
        var description = textarea.getAttribute('data-description');
        textarea.innerText = description;
    }
}

setDescription();