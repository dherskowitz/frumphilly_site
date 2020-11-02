require("alpinejs");
// import 'alpinejs'
// require("./messages");
// require("./navbar");
require("./submit");
require("./events");

let resizeTimer;
window.addEventListener("resize", () => {
    document.body.classList.add("resize-animation-stopper");
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        document.body.classList.remove("resize-animation-stopper");
    }, 400);
});

formatPhone = (e) => {
    var x = e.target.value
        .replace(/\D/g, "")
        .match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
    e.target.value = !x[2]
        ? x[1]
        : "" + x[1] + "-" + x[2] + (x[3] ? "-" + x[3] : "");
};
