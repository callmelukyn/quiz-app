document.addEventListener("DOMContentLoaded", () => {

    const container = document.querySelector(".progress-container");
    if (!container) return;

    const percent = parseInt(container.dataset.percent);
    const circle = document.querySelector(".progress-ring__circle");

    const radius = 70;
    const circumference = 2 * Math.PI * radius;

    circle.style.strokeDasharray = `${circumference}`;
    circle.style.strokeDashoffset = `${circumference}`;

    const offset = circumference - (percent / 100) * circumference;

    requestAnimationFrame(() => {
        circle.style.strokeDashoffset = offset;
    });
});
