/*
    Control Menus Close and Open Buttons
*/
let mainSideBar = document.querySelector(".main-side-bar")
let mainSection = document.querySelector(".main")
let secSideBar = document.querySelector(".sec-side-bar")

// /* Close Main Side Bar */
// document.querySelector("#close-main").addEventListener("click", (event) => {
//     mainSideBar.style.left = "-200px"
//     mainSection.style.left = "10px"

//     document.querySelector("#open-main").style.left = "0";
// })

// /* Open Main Side Bar */
// document.querySelector("#open-main").addEventListener("click", (event) => {
//     mainSideBar.style.left = "10px"
//     mainSection.style.left = "220px"

//     document.querySelector("#open-main").style.left = "-100px";
// })

/* Close Secondary Side Bar */
document.querySelector("#close-sec").addEventListener("click", (event) => {
    secSideBar.style.right = "-400px"
    mainSection.style.right = "10px"

    document.querySelector("#open-sec").style.right = "0";
})

/* Open Secondary Side Bar */
document.querySelector("#open-sec").addEventListener("click", (event) => {
    secSideBar.style.right = "0"
    mainSection.style.right = "410px"

    document.querySelector("#open-sec").style.right = "-100px";
})

/*
    ** Deprecated **
    Since I Made Custom Layout for Login & Signup Pages
    Delete Secondary Side Bar in Login/Register Pages
*/
// // document.addEventListener("load", (event) => {

// if (secSideBar.getAttribute("data-del")) {
//     console.log("not found")
//     secSideBar.style.right = "-400px";
//     mainSection.style.right = "10px";
// }


