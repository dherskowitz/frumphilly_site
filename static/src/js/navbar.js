const navbar__icon = document.querySelector('#navbar__icon');
const menu = document.querySelector('#mobile_nav');
const places = document.querySelector('.algolia-places');

navbar__icon.addEventListener('click', (event) => {
    // document.body.classList.toggle('body--menu-open');
    event.currentTarget.classList.toggle('navbar__icon--open');
    menu.classList.toggle('mobile_nav--open');
    if (places) {
        // If places field on page toggle z-index when menu is open
        if (document.body.classList.contains("body--menu-open")) {
            places.style.zIndex = "-1"
        } else {
            setTimeout(() => {
                places.style.zIndex = "100"
            }, 500);
        }
    }
});
