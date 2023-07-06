/* Show Error Messages */
function showErrorMsg(text) {
    let error = document.querySelector(".error")
    error.querySelector("p").innerHTML = text
    error.classList.add("show")

    setTimeout(function () { error.classList.remove("show") }, 2000)
}

/* Show Success Message */
function showSuccessMsg(text) {
    let success = document.querySelector(".success")
    success.querySelector("p").innerHTML = text
    success.classList.add("show")

    setTimeout(function () { error.classList.remove("show") }, 2000)
}