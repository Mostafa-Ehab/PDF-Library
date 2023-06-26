let book = document.querySelector(".book")
let preview = document.querySelector(".preview")
let maxPageNum = preview.getAttribute("data-num")
let sid = preview.getAttribute("data-sid")
let image = preview.querySelectorAll("div")
let currrentInput = document.querySelector(".page-num input")
let currentPage = currrentInput.value
let maximizeBtn = document.querySelector(".maximize")

/*
    Maximize Preview Button
*/
maximizeBtn.addEventListener("click", () => {
    document.querySelector(".book").classList.toggle("active")
    maximizeBtn.classList.toggle("active")
})

/*
    Page number input
*/
currrentInput.addEventListener("change", function (event) {
    let x = image[currentPage - 1].offsetLeft
    let y = image[currrentInput.value - 1].offsetTop
    book.scrollTo(x, y)
    currentPage = currrentInput.value
})


/*
    Load Image just when needed and change page number with scroll
*/
document.addEventListener("DOMContentLoaded", function (event) {
    book.addEventListener("scroll", function (event) {
        for (let i = 0; i < maxPageNum; i++) {
            if (inViewport(image[i])) {
                // Change Page Nnumber
                currrentInput.value = i + 1
                currentPage = currrentInput.value

                // Render Images
                if (i < (maxPageNum - 10) && i > 10) {
                    for (let n = i - 10; n < i + 10; n++) {
                        if (!image[n + 1].hasChildNodes()) {
                            image[n + 1].innerHTML = `<img src="/book/${sid}/${n + 2}.svg">`
                        }
                    }
                }
            }
        }
    })
})

/*
    Check if Elementin viewport
    Usage: Render images only when needed
*/
function inViewport(el) {
    let rect = el.getBoundingClientRect();

    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) && /* or $(window).height() */
        rect.right <= (window.innerWidth || document.documentElement.clientWidth) /* or $(window).width() */
    );
}

