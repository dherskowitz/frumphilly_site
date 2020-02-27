const message = document.querySelector(".messages");
const dismiss = document.querySelector("#messages__icon");

dismiss && dismiss.addEventListener('click', () => {
    message.classList.add("messages--hiding");
    message.ontransitionend = () => message.parentNode.removeChild(message);
});