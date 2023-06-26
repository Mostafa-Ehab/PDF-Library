/* File Upload Function with progress bar */
const fileInput = document.querySelector("#file")
const submit = document.querySelector("#submit")
const form = document.querySelector("#form")
const sid = document.querySelector("#sid")
const csrf = document.querySelector("#csrf").getAttribute("value")
const confirmFileUpload = document.querySelector(".confirm-file-upload")

fileInput.addEventListener("change", (event) => {
    event.preventDefault()
    let file = fileInput.files[0]
    confirmFileUpload.querySelector("p").innerHTML = file.name
    confirmFileUpload.style.display = "block"
})

confirmFileUpload.querySelector(".file-upload").addEventListener("click", (event) => {
    event.preventDefault()
    /* Configure AJAX Request */
    let file = fileInput.files[0]
    let formData = new FormData()
    formData.append('file', file)

    let xhttp = new XMLHttpRequest()
    xhttp.open('POST', '/admin/add', true)

    // Set Progress bar
    uploadAnimation(xhttp)

    // Change Form Title
    if (document.querySelector("#title").value == "") {
        document.querySelector("#title").value = file.name.slice(0, -4)
    }

    // Send data
    xhttp.setRequestHeader('X-CSRF-Token', csrf);
    xhttp.send(formData);
})

/* Submit Data Form */
submit.addEventListener("click", (event) => {
    event.preventDefault()
    /* Configure AJAX Request */
    let formData = new FormData(form)
    let xhttp = new XMLHttpRequest()
    xhttp.open('POST', '/admin/add', true)
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            console.log(this.responseText)
            if (this.responseText == "404") {
                showErrorMsg("An Error has occured, check your Inputs (:")
            } else {
                showSuccessMsg("Book Added Successfully (:")
                setTimeout(function () {
                    location.assign("/admin")
                }, 3000)
            }
        }
    }
    // Send data
    xhttp.setRequestHeader('X-CSRF-Token', csrf)
    xhttp.send(formData)
})

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

function uploadAnimation(xhttp) {
    let animationContainer = document.querySelector(".upload-animation")

    // Hide Upload form and show progress bars
    document.querySelector(".upload-container form label").style.display = "none"
    confirmFileUpload.style.display = "none"
    fileInput.setAttribute("disabled", "on")
    animationContainer.style.display = "block";

    // File Upload Animation
    animationContainer.querySelector(".upload-icon").style.color = "var(--blue-color)"
    xhttp.upload.onprogress = (e) => {
        if (e.lengthComputable) {
            let percentComplete = (e.loaded / e.total) * 100;
            // animationContainer.querySelector(".upload-icon p").innerText = `${percentComplete}/100%`;
            animationContainer.querySelector(".upload-bar span").style.width = `${percentComplete}%`;
        }
    }

    // After File Uploading
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText == "404") {
                showErrorMsg("An Error has occured, check your file type (:")
                setTimeout(function () {
                    location.assign("/admin/add")
                }, 3000)
                return
            }
            sid.setAttribute("value", this.responseText)
            animationContainer.querySelector(".upload-icon span").innerText = "Uploaded"

            // Activate Submit Button
            submit.classList.remove("disabled")
            submit.removeAttribute("disabled")

            // File Processing Animation
            animationContainer.querySelector(".processing-icon").style.color = "var(--red-color)"
            animationContainer.querySelector(".processing-icon span").innerText = "Processing..."

            let progressInterval = setInterval(function () {
                let xhttp2 = new XMLHttpRequest()
                xhttp2.open('GET', '/admin/progress?sid=' + sid.value, true)
                xhttp2.onreadystatechange = function () {
                    if (this.readyState == 4 && this.status == 200) {
                        let progress = JSON.parse(this.responseText)
                        let percentComplete = (progress[0] / progress[1]) * 100;
                        // animationContainer.querySelector(".processing-icon p").innerText = `${percentComplete}/100%`;
                        animationContainer.querySelector(".processing-bar span").style.width = `${percentComplete}%`;

                        // Done Animation
                        if (progress[0] == progress[1]) {
                            clearInterval(progressInterval)
                            setTimeout(() => {
                                animationContainer.querySelector(".processing-icon span").innerText = "Processed"
                                animationContainer.querySelector(".done-icon").style.color = "var(--green-color)"
                                // animationContainer.querySelector(".done-icon p").innerText = `${percentComplete}/100%`;
                                animationContainer.querySelector(".done-bar span").style.width = "100%"
                            }, 2000)
                        }
                    }
                }
                xhttp2.setRequestHeader('X-CSRF-Token', csrf)
                xhttp2.send()
            }, 2000)
        }
    }
}

