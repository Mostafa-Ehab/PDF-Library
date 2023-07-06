const search = document.querySelector("#search")
const container = document.querySelector("#container")

if (search) {
    search.addEventListener("input", function (event) {
        console.log("Hello")
        let q = search.value
        let xhttp = new XMLHttpRequest()
        xhttp.open("GET", "?q=" + q + "&no-render=true", true)
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                container.innerHTML = this.responseText
            }
        }
        xhttp.send()
    })
}