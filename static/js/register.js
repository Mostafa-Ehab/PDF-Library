const error = document.querySelector(".error")
const csrf = document.querySelector("#csrf").value

document.querySelector(".submit").addEventListener("click", function (event) {
    event.preventDefault()
    error.innerHTML = ""

    let username = document.querySelector("#username").value
    let email = document.querySelector("#email").value
    let password = document.querySelector("#password").value
    let passwordConf = document.querySelector("#password-conf").value

    if (email) {
        if (!checkEmail(email)) {
            error.innerHTML = "Please enter a valid email"
            return
        }
    }

    if (!username && !email) {
        error.innerHTML = "Please enter either username or email"
        return
    }

    if (!password) {
        error.innerHTML = "Password can't be empty"
        return
    }

    if (password != passwordConf) {
        error.innerHTML = "Passwords don't match"
        return
    }

    let formData = new FormData(document.querySelector(".register"))
    let xhttp = new XMLHttpRequest()
    xhttp.open("POST", "/register", true)
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText != "200") {
                error.innerHTML = this.responseText
            } else {
                location.assign("/")
            }
        }
    }
    xhttp.setRequestHeader("X-CSRF-Token", csrf)
    xhttp.send(formData)
})

function checkEmail(text) {
    var validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    if (text.match(validRegex)) {
        return true;

    } else {
        return false;
    }
}