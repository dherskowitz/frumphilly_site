let form = document.querySelector(".form");

if (form && document.getElementById("id_location")) {
    // trix wysiwyg editor prevent file upload
    addEventListener("trix-file-accept", function (event) {
        event.preventDefault();
    });
}
