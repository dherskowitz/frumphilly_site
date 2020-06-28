if (document.getElementById("id_email")) {
    document.getElementById("id_email").focus();
}

let submitBtn = document.querySelector(".btn--form-submit");
let loader = document.querySelector(".btn-loader");
let signupForm = document.querySelector("#signup-form");
let loginForm = document.querySelector("#login-form");
let events_form = document.querySelector(".events_form");

function showLoading() {
    submitBtn.firstElementChild.remove();
    loader.style.display = "block";
}
if (signupForm) {
    signupForm.addEventListener("submit", showLoading);
}
if (loginForm) {
    loginForm.addEventListener("submit", showLoading);
}
if (events_form) {
    events_form.addEventListener("submit", showLoading);
}

