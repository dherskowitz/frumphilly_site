const navbar__icon = document.querySelector('#navbar__icon');
const navbar__nav = document.querySelector('#navbar__nav');
navbar__icon.addEventListener('click', (event) => {
    document.body.classList.toggle('body--menu-open');
    event.currentTarget.classList.toggle('navbar__icon--open');
    navbar__nav.classList.toggle('navbar__nav--open');
});