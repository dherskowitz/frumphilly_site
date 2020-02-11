const nav_menu_icon = document.querySelector('#nav_menu_icon');
const navbar__nav = document.querySelector('#navbar__nav');
nav_menu_icon.addEventListener('click', (event) => {
    document.body.classList.toggle('menu-open');
    event.currentTarget.classList.toggle('open');
    navbar__nav.classList.toggle('open');
});