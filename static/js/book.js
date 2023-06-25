/*
    Maximize Preview Button
*/
let maximizeBtn = document.querySelector(".maximize")
maximizeBtn.addEventListener("click", () => {
    document.querySelector(".book").classList.toggle("active")
    maximizeBtn.classList.toggle("active")
})
