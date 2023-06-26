/*
    Maximize Preview Button
*/
let maximizeBtn = document.querySelector(".maximize")
maximizeBtn.addEventListener("click", () => {
    document.querySelector(".book").classList.toggle("active")
    maximizeBtn.classList.toggle("active")
})


document.addEventListener("DOMContentLoaded", function (event) {
    let book = document.querySelector(".book")
    let preview = document.querySelector(".preview")
    let pagesNum = preview.getAttribute("data-num")
    let sid = preview.getAttribute("data-sid")
    let image = preview.querySelectorAll("div")
    let current = 0

    book.addEventListener("scroll", function (event) {
        for (let i = current; i < pagesNum; i++) {
            if (inViewport(image[i]) && i > current) {
                current = i
                console.log(i)
                if (!image[i + 1].hasChildNodes()) {
                    // let node = `<img src="/book/${sid}/${i + 2}.svg">`
                    // image[i + 1].innerHTML = node

                    // node = `<img src="/book/${sid}/${i + 3}.svg">`
                    // image[i + 2].innerHTML = node

                    // node = `<img src="/book/${sid}/${i + 4}.svg">`
                    // image[i + 3].innerHTML = node
                    for (let n = 1; n <= 10; n++) {
                        if (i + n < pagesNum) {
                            image[i + n].innerHTML = `<img src="/book/${sid}/${i + n + 1}.svg">`
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
    // Special bonus for those using jQuery
    // if (typeof jQuery === "function" && el instanceof jQuery) {
    //     el = el[0];
    // }

    let rect = el.getBoundingClientRect();

    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) && /* or $(window).height() */
        rect.right <= (window.innerWidth || document.documentElement.clientWidth) /* or $(window).width() */
    );
}

