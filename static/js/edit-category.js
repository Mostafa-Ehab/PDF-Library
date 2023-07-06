let action = document.querySelector(".form").getAttribute("action")

document.querySelector("#submit").addEventListener("click", function (event) {
    event.preventDefault()
    let formData = new FormData(document.querySelector(".form"))
    let xhttp = new XMLHttpRequest()
    xhttp.open("POST", action, true)
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText != "200") {
                showErrorMsg(this.responseText)
            } else {
                showSuccessMsg("Category Saved Successfully")
                setTimeout(() => {
                    location.assign("/admin")
                }, 3000)
            }
        }
    }
    // Send data
    xhttp.setRequestHeader('X-CSRF-Token', csrf)
    xhttp.send(formData)
})