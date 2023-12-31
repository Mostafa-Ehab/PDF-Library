/*
    Control Menus Close and Open Buttons
*/
let mainSideBar = document.querySelector(".main-side-bar")
let mainSection = document.querySelector(".main")
let secSideBar = document.querySelector(".sec-side-bar")

/* Close Main Side Bar */
/*
** ** Deprecated **
** Close Button have display None
*/
document.querySelector("#close-main").addEventListener("click", (event) => {
    mainSideBar.classList.remove("active")

    document.querySelector("#close-main").style.display = "none"
})

/* Open Main Side Bar */
/*
** ** Deprecated **
** Close Button have display None
*/
document.querySelector("#open-main").addEventListener("click", (event) => {
    mainSideBar.classList.add("active")

    document.querySelector("#close-main").style.display = "block"
})

/* Close Secondary Side Bar */
document.querySelector("#close-sec").addEventListener("click", (event) => {
    secSideBar.classList.remove("active")
    mainSection.classList.add("expand")

    document.querySelector("#open-sec").style.right = "0"
})

/* Open Secondary Side Bar */
document.querySelector("#open-sec").addEventListener("click", (event) => {
    secSideBar.classList.add("active")
    mainSection.classList.remove("expand")

    document.querySelector("#open-sec").style.right = "-100px"
})

/* Close Secondary Side Bar By default */
document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#open-sec").style.right = "0"
})
