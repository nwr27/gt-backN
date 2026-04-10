document.addEventListener("DOMContentLoaded", function () {
  const firstAutofocus = document.querySelector("input[autofocus], input[type='text'], input[type='number']");
  if (firstAutofocus && !firstAutofocus.value) {
    firstAutofocus.focus();
  }

  const alerts = document.querySelectorAll(".alert[data-autohide='true']");
  alerts.forEach((el) => {
    setTimeout(() => {
      el.style.transition = "opacity 0.3s ease";
      el.style.opacity = "0";
      setTimeout(() => {
        el.remove();
      }, 300);
    }, 2500);
  });
});