document.querySelector("#delete").addEventListener("click", function (event) {
    document.querySelector(".modal").classList.add("active")
})

document.querySelector(".modal .no").addEventListener("click", function (event) {
    document.querySelector(".modal").classList.remove("active")
})

document.querySelector(".category button").addEventListener("click", function (event) {
    event.preventDefault()
    document.querySelector(".category ul").classList.toggle("active")
})

